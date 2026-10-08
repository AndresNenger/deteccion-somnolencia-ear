"""Procesa un video y genera el video anotado + CSV con el EAR por fotograma.

Uso:
    python scripts/process_video.py videoplayback.mp4 -o resultado.mp4 --csv ear.csv
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from somnolencia.detector import (  # noqa: E402
    DEFAULT_CONSECUTIVE_FRAMES,
    DEFAULT_EAR_THRESHOLD,
)
from somnolencia.pipeline import process_video  # noqa: E402


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument("video", help="ruta del video de entrada")
    p.add_argument("-o", "--output", default="resultado.mp4")
    p.add_argument("--csv", default=None, help="guardar EAR por fotograma en este CSV")
    p.add_argument("--threshold", type=float, default=DEFAULT_EAR_THRESHOLD)
    p.add_argument("--frames", type=int, default=DEFAULT_CONSECUTIVE_FRAMES,
                   help="fotogramas consecutivos con EAR bajo para activar la alerta")
    p.add_argument("--max-frames", type=int, default=None)
    args = p.parse_args()

    r = process_video(
        args.video, args.output, args.threshold, args.frames,
        csv_path=args.csv, max_frames=args.max_frames,
    )
    print("Video terminado.")
    print(f"  Fotogramas:            {r['frames']} ({r['fps']:.1f} fps)")
    print(f"  Con rostro detectado:  {r['frames_con_rostro']}")
    print(f"  Fotogramas en alerta:  {r['frames_somnolientos']}")
    print(f"  Eventos de alerta:     {r['eventos_alerta']}")
    print(f"  Salida:                {r['salida']}")


if __name__ == "__main__":
    main()
