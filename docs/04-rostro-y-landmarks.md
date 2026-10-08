# 04 · Detección del rostro y landmarks

**Objetivo:** obtener los 478 puntos de referencia faciales con MediaPipe Face Landmarker.

## Qué es un landmark

Un punto con significado anatómico fijo (esquina del ojo, punta de la nariz…). MediaPipe devuelve **478 puntos** por rostro con coordenadas `x`, `y` **normalizadas** (0–1 respecto al ancho/alto de la imagen) y `z` (profundidad relativa).

## Crear el detector

```python
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision

opciones = vision.FaceLandmarkerOptions(
    base_options=mp_python.BaseOptions(model_asset_path="face_landmarker.task"),
    running_mode=vision.RunningMode.VIDEO,
    num_faces=1,
)
detector = vision.FaceLandmarker.create_from_options(opciones)
```

El modelo `face_landmarker.task` se descarga de
`https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task`
(el código lo hace solo, ver [`face.py`](../src/somnolencia/face.py)).

### ¿Por qué modo `VIDEO`?

| Modo | Uso |
|---|---|
| `IMAGE` | Fotos sueltas; detecta desde cero cada vez |
| **`VIDEO`** | **Videos: reutiliza el seguimiento entre fotogramas (más rápido y estable)** |
| `LIVE_STREAM` | Cámara en vivo con callbacks asíncronos |

En modo `VIDEO` hay que pasar un **timestamp en milisegundos estrictamente creciente**: `int(indice * 1000 / fps)`.

## Procesar un fotograma

```python
rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)          # OpenCV es BGR, MediaPipe espera RGB
imagen = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
resultado = detector.detect_for_video(imagen, int(t_ms))

if len(resultado.face_landmarks) > 0:                  # ¿hubo rostro?
    cara = resultado.face_landmarks[0]                 # lista de 478 puntos
```

## Cuando no hay rostro

`face_landmarks` viene vacío (cara tapada, de perfil, fuera de cuadro). El proyecto lo trata como estado **`SIN ROSTRO`** y **reinicia el contador**: no hay evidencia de que los ojos estén cerrados, y no queremos acumular una alerta con datos inexistentes.

## Wrapper del proyecto

[`FaceLandmarkerWrapper`](../src/somnolencia/face.py) encapsula todo lo anterior:

```python
from somnolencia.face import FaceLandmarkerWrapper

with FaceLandmarkerWrapper() as lm:
    puntos = lm.process(frame_bgr, timestamp_ms)   # array (478, 2) o None
```
