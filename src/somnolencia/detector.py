"""Logica de alerta: EAR bajo el umbral durante N fotogramas consecutivos."""

from __future__ import annotations

from dataclasses import dataclass

DEFAULT_EAR_THRESHOLD = 0.22
DEFAULT_CONSECUTIVE_FRAMES = 15

ESTADO_DESPIERTO = "DESPIERTO"
ESTADO_SOMNOLIENTO = "SOMNOLIENTO"
ESTADO_SIN_ROSTRO = "SIN ROSTRO"


@dataclass(frozen=True)
class DrowsinessState:
    ear: float | None
    counter: int
    drowsy: bool
    label: str


class DrowsinessDetector:
    """Maquina de estados minima.

    - EAR >= umbral  -> ojo abierto: el contador se reinicia a 0.
    - EAR <  umbral  -> ojo cerrado: el contador aumenta en 1.
    - contador > N   -> SOMNOLIENTO (se activa la alerta).
    - Sin rostro     -> se reinicia el contador (no hay evidencia de cierre).
    """

    def __init__(
        self,
        ear_threshold: float = DEFAULT_EAR_THRESHOLD,
        consecutive_frames: int = DEFAULT_CONSECUTIVE_FRAMES,
    ) -> None:
        if ear_threshold <= 0:
            raise ValueError("ear_threshold debe ser positivo")
        if consecutive_frames < 1:
            raise ValueError("consecutive_frames debe ser >= 1")
        self.ear_threshold = ear_threshold
        self.consecutive_frames = consecutive_frames
        self.counter = 0

    def reset(self) -> None:
        self.counter = 0

    def update(self, ear: float | None) -> DrowsinessState:
        """Procesa el EAR de un fotograma (``None`` si no hubo rostro)."""
        if ear is None:
            self.counter = 0
            return DrowsinessState(None, 0, False, ESTADO_SIN_ROSTRO)

        if ear < self.ear_threshold:
            self.counter += 1
        else:
            self.counter = 0

        drowsy = self.counter > self.consecutive_frames
        label = ESTADO_SOMNOLIENTO if drowsy else ESTADO_DESPIERTO
        return DrowsinessState(ear, self.counter, drowsy, label)


def frames_from_seconds(seconds: float, fps: float) -> int:
    """Convierte una duracion en segundos al numero de fotogramas equivalente.

    Util porque 15 fotogramas son 0.5 s a 30 fps pero 1 s a 15 fps.
    """
    return max(1, round(seconds * fps))
