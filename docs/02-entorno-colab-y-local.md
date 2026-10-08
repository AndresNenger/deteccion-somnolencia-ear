# 02 · Entorno: Google Colab y local

**Objetivo:** tener el proyecto corriendo.

## Opción A · Google Colab (recomendada)

1. Abre el notebook con el botón del [README](../README.md) (**Abrir en Colab**), o ve a <https://colab.research.google.com> → *Archivo → Abrir cuaderno → GitHub* y pega la URL de tu repositorio.
2. Ejecuta las celdas **en orden** (`Ctrl + Enter`, o *Entorno de ejecución → Ejecutar todo*).
3. La primera celda instala MediaPipe (`!pip install -q mediapipe`). Si Colab pide reiniciar el entorno, hazlo y vuelve a ejecutar desde el principio.
4. En la celda del Paso 1, elige `FUENTE` (`"subir"`, `"drive"`, `"url"` o `"ruta"`).

No necesitas GPU: el modelo corre en CPU a una velocidad razonable.

## Opción B · Instalación local

```bash
git clone https://github.com/AndresNenger/deteccion-somnolencia-ear.git
cd deteccion-somnolencia-ear
python -m venv .venv
```

Activa el entorno virtual:

```bash
# Linux / macOS
source .venv/bin/activate
```

```powershell
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

```bash
pip install -r requirements.txt
pip install -e .
pytest -q
```

Si `pytest` muestra todo en verde, el cálculo del EAR y la lógica de alerta funcionan.

## Procesar un video desde la terminal

```bash
python scripts/process_video.py mi_video.mp4 -o resultado.mp4 --csv ear.csv
```

La primera ejecución descarga `face_landmarker.task` (~4 MB) en `models/`.

Parámetros útiles: `--threshold 0.22`, `--frames 15`, `--max-frames 300`.

## Webcam en vivo (solo local)

```bash
python scripts/live_webcam.py
```

Pulsa `q` para salir. En Colab no hay acceso directo a la cámara con OpenCV.

## Problemas frecuentes

| Síntoma | Causa probable | Solución |
|---|---|---|
| `No se pudo abrir el video` | Ruta incorrecta o códec no soportado | Revisa la ruta; reconvierte el video a H.264 |
| `SIN ROSTRO` en todos los fotogramas | Cara de perfil, muy lejos o a oscuras | Usa un video frontal con buena luz |
| El video de salida no se reproduce en el navegador | Códec `mp4v` | La celda del Paso 8 lo reconvierte con ffmpeg a H.264 |
| `ModuleNotFoundError: mediapipe` | Dependencias sin instalar | `pip install mediapipe` |
