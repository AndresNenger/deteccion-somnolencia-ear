# 06 · Lógica de alerta: umbral + contador

**Objetivo:** convertir el EAR de cada fotograma en la decisión DESPIERTO / SOMNOLIENTO.

## Reglas

| Condición en el fotograma | Efecto |
|---|---|
| `EAR >= 0.22` (ojo abierto) | `contador = 0` |
| `EAR < 0.22` (ojo cerrado) | `contador += 1` |
| `contador > 15` | Estado **SOMNOLIENTO** → se activa la alerta |
| Sin rostro | `contador = 0`, estado **SIN ROSTRO** |

```python
if ear is None:
    contador = 0
    estado = "SIN ROSTRO"
else:
    contador = contador + 1 if ear < UMBRAL_EAR else 0
    estado = "SOMNOLIENTO" if contador > FRAMES_CONSECUTIVOS else "DESPIERTO"
```

## Ejemplo con 30 fps (N = 15)

```
EAR:      0.30 0.30 0.10 0.10 0.10 0.30 0.10 ... (16 veces seguidas) ...
contador:   0    0    1    2    3    0    1  ...  16
estado:   DESP DESP DESP DESP DESP DESP DESP ... SOMNOLIENTO
```

El cierre corto (3 fotogramas) **no** alerta; el sostenido (16) **sí**. Estos casos están cubiertos en [`tests/test_detector.py`](../tests/test_detector.py).

## Los dos parámetros

| Parámetro | Por defecto | Subirlo… | Bajarlo… |
|---|---|---|---|
| `UMBRAL_EAR` | 0.22 | …detecta más cierres, pero más falsos positivos | …exige un cierre más marcado |
| `FRAMES_CONSECUTIVOS` | 15 | …más tolerante, alerta más tarde | …alerta antes, más falsas alarmas por parpadeos |

## De fotogramas a segundos

15 fotogramas no son siempre el mismo tiempo:

| fps | 15 fotogramas = |
|---|---|
| 30 | 0,5 s |
| 24 | 0,63 s |
| 15 | 1,0 s |

Si quieres un criterio **en segundos** independiente del video:

```python
from somnolencia import frames_from_seconds
N = frames_from_seconds(0.5, fps)     # 15 a 30 fps, 12 a 24 fps
```

## Eventos vs. fotogramas

Mientras dure el cierre, cada fotograma posterior al 15.º está en alerta. Para contar **cuántas alertas distintas** hubo, se cuenta solo el *flanco de subida* (paso de no-somnoliento a somnoliento). El resumen de `process_video` devuelve ambos: `frames_somnolientos` y `eventos_alerta`.

## Implementación

[`DrowsinessDetector`](../src/somnolencia/detector.py) es una máquina de estados mínima, separada del video y de MediaPipe, por eso se puede probar con números sintéticos sin ningún video.
