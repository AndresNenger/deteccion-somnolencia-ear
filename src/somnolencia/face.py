"""Deteccion de rostro y landmarks con MediaPipe Face Landmarker (478 puntos)."""

from __future__ import annotations

import urllib.request
from pathlib import Path

import numpy as np

MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/face_landmarker/"
    "face_landmarker/float16/1/face_landmarker.task"
)
DEFAULT_MODEL_PATH = Path("models") / "face_landmarker.task"


def download_model(path: str | Path = DEFAULT_MODEL_PATH) -> Path:
    """Descarga el modelo ``face_landmarker.task`` si aun no existe."""
    path = Path(path)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        print(f"Descargando modelo en {path} ...")
        urllib.request.urlretrieve(MODEL_URL, path)
    return path


class FaceLandmarkerWrapper:
    """Envoltorio sencillo: ``process(frame_bgr, timestamp_ms)`` -> landmarks o None.

    Se usa el modo VIDEO de MediaPipe, que aprovecha la coherencia temporal
    entre fotogramas (seguimiento) y exige timestamps crecientes.
    """

    def __init__(self, model_path: str | Path = DEFAULT_MODEL_PATH, num_faces: int = 1) -> None:
        import mediapipe as mp
        from mediapipe.tasks import python as mp_python
        from mediapipe.tasks.python import vision

        self._mp = mp
        options = vision.FaceLandmarkerOptions(
            base_options=mp_python.BaseOptions(model_asset_path=str(download_model(model_path))),
            running_mode=vision.RunningMode.VIDEO,
            num_faces=num_faces,
        )
        self._landmarker = vision.FaceLandmarker.create_from_options(options)

    def process(self, frame_bgr: np.ndarray, timestamp_ms: int) -> np.ndarray | None:
        """Devuelve un array (478, 2) de coordenadas normalizadas, o ``None``."""
        import cv2

        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        image = self._mp.Image(image_format=self._mp.ImageFormat.SRGB, data=rgb)
        result = self._landmarker.detect_for_video(image, int(timestamp_ms))
        if not result.face_landmarks:
            return None
        face = result.face_landmarks[0]
        return np.array([[p.x, p.y] for p in face], dtype=float)

    def close(self) -> None:
        self._landmarker.close()

    def __enter__(self) -> "FaceLandmarkerWrapper":
        return self

    def __exit__(self, *exc) -> None:
        self.close()
