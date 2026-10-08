"""Deteccion en tiempo real con la webcam (solo local, no funciona en Colab).

Uso:
    python scripts/live_webcam.py [--camera 0]
Presiona 'q' para salir.
"""

import argparse
import sys
import time
from pathlib import Path

import cv2

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from somnolencia.detector import (  # noqa: E402
    DEFAULT_CONSECUTIVE_FRAMES,
    DEFAULT_EAR_THRESHOLD,
    DrowsinessDetector,
)
from somnolencia.ear import LEFT_EYE, RIGHT_EYE, landmarks_to_pixels, mean_ear  # noqa: E402
from somnolencia.face import FaceLandmarkerWrapper  # noqa: E402
from somnolencia.pipeline import draw_overlay  # noqa: E402


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument("--camera", type=int, default=0)
    p.add_argument("--threshold", type=float, default=DEFAULT_EAR_THRESHOLD)
    p.add_argument("--frames", type=int, default=DEFAULT_CONSECUTIVE_FRAMES)
    args = p.parse_args()

    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        sys.exit(f"No se pudo abrir la camara {args.camera}")

    detector = DrowsinessDetector(args.threshold, args.frames)
    t0 = time.monotonic()
    with FaceLandmarkerWrapper() as landmarker:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            h, w = frame.shape[:2]
            lm = landmarker.process(frame, int((time.monotonic() - t0) * 1000))
            ear, eyes = None, []
            if lm is not None:
                px = landmarks_to_pixels(lm, w, h)
                ear = mean_ear(px)[0]
                eyes = [px[LEFT_EYE], px[RIGHT_EYE]]
            state = detector.update(ear)
            cv2.imshow("Somnolencia (q para salir)", draw_overlay(frame, state, args.frames, eyes))
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
