# 03 · Video de entrada y lectura de fotogramas

**Objetivo:** abrir un video y recorrerlo fotograma a fotograma con OpenCV.

## Abrir el video

```python
import cv2

cap = cv2.VideoCapture("videoplayback.mp4")
if not cap.isOpened():
    print("Error: No se pudo abrir el video")
else:
    print("Video abierto correctamente")
```

`VideoCapture` **no lanza excepción** si falla: solo devuelve un objeto "cerrado". Por eso se comprueba `isOpened()`.

## Propiedades útiles

```python
fps   = cap.get(cv2.CAP_PROP_FPS) or 30.0          # algunos archivos devuelven 0
ancho = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
alto  = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
```

El `fps` importa: el umbral de "15 fotogramas" equivale a **0,5 s a 30 fps** pero a **1 s a 15 fps** ([doc 06](06-logica-de-alerta.md)).

## Leer cada fotograma

```python
while True:
    ret, frame = cap.read()
    if not ret:        # fin del video (o error de lectura)
        break
    # ... procesar `frame` ...
cap.release()
```

`frame` es un arreglo NumPy `(alto, ancho, 3)` en orden de canales **BGR** (no RGB). Es el error más común al mezclar OpenCV con otras librerías.

## Cargar el video en Colab

| `FUENTE` | Cuándo usarla |
|---|---|
| `"subir"` | Archivos pequeños; se pierden al cerrar la sesión |
| `"drive"` | Archivos grandes o reutilizables; requiere autorizar acceso a Drive |
| `"url"` | Enlace directo a un `.mp4` (no una página de YouTube) |
| `"ruta"` | El archivo ya está en `/content` |

## Consejos para un buen video

- Cámara frontal, a la altura del rostro, cara llenando una buena parte del cuadro.
- Luz uniforme (evita contraluz).
- Resolución 480p–720p es suficiente; más resolución solo hace el proceso más lento.
- **Privacidad:** usa solo videos propios o con consentimiento de quienes aparecen.
