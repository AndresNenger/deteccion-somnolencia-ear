"""Calculo del Eye Aspect Ratio (EAR).

El EAR (Soukupova y Cech, 2016) resume la apertura de un ojo con 6 puntos:

            p2   p3
       p1              p4
            p6   p5

    EAR = (||p2 - p6|| + ||p3 - p5||) / (2 * ||p1 - p4||)

Ojo abierto -> EAR alto (~0.25-0.35). Ojo cerrado -> EAR cercano a 0.
"""

from __future__ import annotations

import numpy as np

# Indices de MediaPipe Face Landmarker (malla de 478 puntos), en el orden
# p1, p2, p3, p4, p5, p6 de la formula del EAR.
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]


def eye_aspect_ratio(eye: np.ndarray) -> float:
    """EAR de un ojo a partir de sus 6 puntos (array de forma (6, 2)).

    Los puntos deben estar en pixeles (no normalizados 0-1): si no, la
    relacion de aspecto de la imagen deforma las distancias.
    """
    eye = np.asarray(eye, dtype=float)
    if eye.shape != (6, 2):
        raise ValueError(f"Se esperaban 6 puntos 2D, llego {eye.shape}")

    a = np.linalg.norm(eye[1] - eye[5])  # distancia vertical p2-p6
    b = np.linalg.norm(eye[2] - eye[4])  # distancia vertical p3-p5
    c = np.linalg.norm(eye[0] - eye[3])  # distancia horizontal p1-p4
    if c == 0:
        return 0.0
    return float((a + b) / (2.0 * c))


def landmarks_to_pixels(landmarks_norm: np.ndarray, width: int, height: int) -> np.ndarray:
    """Convierte landmarks normalizados (N, 2) en coordenadas de pixel."""
    pts = np.asarray(landmarks_norm, dtype=float)[:, :2]
    return pts * np.array([width, height], dtype=float)


def mean_ear(
    landmarks_px: np.ndarray,
    left_idx: list[int] = LEFT_EYE,
    right_idx: list[int] = RIGHT_EYE,
) -> tuple[float, float, float]:
    """Devuelve (ear_promedio, ear_izquierdo, ear_derecho)."""
    left = eye_aspect_ratio(landmarks_px[left_idx])
    right = eye_aspect_ratio(landmarks_px[right_idx])
    return (left + right) / 2.0, left, right
