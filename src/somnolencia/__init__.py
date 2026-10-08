"""Deteccion de somnolencia en conductores con vision por computadora (EAR + MediaPipe)."""

from .detector import (
    DEFAULT_CONSECUTIVE_FRAMES,
    DEFAULT_EAR_THRESHOLD,
    DrowsinessDetector,
    DrowsinessState,
    frames_from_seconds,
)
from .ear import LEFT_EYE, RIGHT_EYE, eye_aspect_ratio, landmarks_to_pixels, mean_ear

__version__ = "0.1.0"

__all__ = [
    "DEFAULT_CONSECUTIVE_FRAMES",
    "DEFAULT_EAR_THRESHOLD",
    "DrowsinessDetector",
    "DrowsinessState",
    "LEFT_EYE",
    "RIGHT_EYE",
    "eye_aspect_ratio",
    "frames_from_seconds",
    "landmarks_to_pixels",
    "mean_ear",
]
