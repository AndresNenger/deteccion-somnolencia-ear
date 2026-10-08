"""Pipeline completo: video de entrada -> EAR -> alerta -> video de salida."""

from __future__ import annotations

import csv
import shutil
import subprocess
from collections.abc import Iterable
from pathlib import Path

import cv2
import numpy as np

from .detector import (
    DEFAULT_CONSECUTIVE_FRAMES,
    DEFAULT_EAR_THRESHOLD,
    DrowsinessDetector,
    DrowsinessState,
)
from .ear import LEFT_EYE, RIGHT_EYE, landmarks_to_pixels, mean_ear
from .face import DEFAULT_MODEL_PATH, FaceLandmarkerWrapper

GREEN = (0, 255, 0)
RED = (0, 0, 255)
ORANGE = (0, 165, 255)
WHITE = (255, 255, 255)
FONT = cv2.FONT_HERSHEY_SIMPLEX  # no admite tildes ni ene: textos sin acentos


def draw_overlay(
    frame: np.ndarray,
    state: DrowsinessState,
    consecutive_frames: int,
    eye_points: Iterable[np.ndarray] = (),
) -> np.ndarray:
    """Dibuja puntos de los ojos, EAR, contador, estado y alerta sobre el frame."""
    for eye in eye_points:
        for x, y in eye:
            cv2.circle(frame, (int(x), int(y)), 2, GREEN, -1)

    ear_txt = "--" if state.ear is None else f"{state.ear:.2f}"
    cv2.putText(frame, f"EAR: {ear_txt}", (20, 30), FONT, 0.8, WHITE, 2)
    cv2.putText(
        frame, f"Contador: {state.counter}/{consecutive_frames}", (20, 60), FONT, 0.7, ORANGE, 2
    )
    color = RED if state.drowsy else GREEN
    cv2.putText(frame, state.label, (20, 95), FONT, 0.9, color, 2)

    if state.drowsy:
        h, w = frame.shape[:2]
        cv2.putText(frame, "ALERTA", (w // 2 - 110, h // 2), FONT, 2.0, RED, 5)
    return frame


def reencode_h264(path: str | Path) -> Path:
    """Reencoda con ffmpeg a H.264 para poder reproducirlo en el navegador/Colab.

    OpenCV escribe con el codec ``mp4v``, que Chrome y Colab no reproducen.
    Si no hay ffmpeg, devuelve el archivo original sin cambios.
    """
    path = Path(path)
    if shutil.which("ffmpeg") is None:
        print("ffmpeg no disponible: se deja el video con codec mp4v.")
        return path
    tmp = path.with_name(path.stem + "_h264.mp4")
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(path),
         "-vcodec", "libx264", "-pix_fmt", "yuv420p", str(tmp)],
        check=True,
    )
    tmp.replace(path)
    return path


def process_video(
    input_path: str | Path,
    output_path: str | Path = "resultado.mp4",
    ear_threshold: float = DEFAULT_EAR_THRESHOLD,
    consecutive_frames: int = DEFAULT_CONSECUTIVE_FRAMES,
    model_path: str | Path = DEFAULT_MODEL_PATH,
    csv_path: str | Path | None = None,
    max_frames: int | None = None,
    h264: bool = True,
) -> dict:
    """Procesa un video y escribe el resultado anotado.

    Devuelve un resumen con ``frames``, ``fps``, ``frames_con_rostro``,
    ``frames_somnolientos``, ``eventos_alerta`` y la lista ``registros``
    (un dict por fotograma: frame, tiempo_s, ear, contador, estado).
    """
    cap = cv2.VideoCapture(str(input_path))
    if not cap.isOpened():
        raise FileNotFoundError(f"No se pudo abrir el video: {input_path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    writer = cv2.VideoWriter(
        str(output_path), cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height)
    )

    detector = DrowsinessDetector(ear_threshold, consecutive_frames)
    registros: list[dict] = []
    eventos = 0
    previo_somnoliento = False
    idx = 0

    with FaceLandmarkerWrapper(model_path) as landmarker:
        while True:
            ok, frame = cap.read()
            if not ok or (max_frames is not None and idx >= max_frames):
                break

            lm = landmarker.process(frame, int(idx * 1000 / fps))
            eyes: list[np.ndarray] = []
            ear: float | None = None
            if lm is not None:
                px = landmarks_to_pixels(lm, width, height)
                ear, _, _ = mean_ear(px)
                eyes = [px[LEFT_EYE], px[RIGHT_EYE]]

            state = detector.update(ear)
            if state.drowsy and not previo_somnoliento:
                eventos += 1  # flanco de subida: una alerta nueva
            previo_somnoliento = state.drowsy

            writer.write(draw_overlay(frame, state, consecutive_frames, eyes))
            registros.append(
                {
                    "frame": idx,
                    "tiempo_s": round(idx / fps, 3),
                    "ear": None if state.ear is None else round(state.ear, 4),
                    "contador": state.counter,
                    "estado": state.label,
                }
            )
            idx += 1

    cap.release()
    writer.release()
    if h264:
        reencode_h264(output_path)

    if csv_path is not None:
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["frame", "tiempo_s", "ear", "contador", "estado"])
            w.writeheader()
            w.writerows(registros)

    return {
        "frames": idx,
        "fps": fps,
        "frames_con_rostro": sum(r["ear"] is not None for r in registros),
        "frames_somnolientos": sum(r["estado"] == "SOMNOLIENTO" for r in registros),
        "eventos_alerta": eventos,
        "salida": str(output_path),
        "registros": registros,
    }
