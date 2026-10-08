# 01 · Teoría: Eye Aspect Ratio (EAR)

**Objetivo:** entender qué mide el EAR antes de escribir código.

## La idea

Un ojo abierto es "alto y ancho"; un ojo cerrado es "ancho pero casi sin altura". Si dividimos la altura entre el ancho, obtenemos un número que cae cuando el ojo se cierra y que **no depende de qué tan cerca esté la cara de la cámara** (la razón es adimensional).

## Los 6 puntos

```
        p2    p3
   p1                p4
        p6    p5
```

- `p1` y `p4`: comisuras (esquinas) del ojo → distancia **horizontal** `C`.
- `p2–p6` y `p3–p5`: pares de puntos de párpado superior/inferior → distancias **verticales** `A` y `B`.

## La fórmula (Soukupová y Čech, 2016)

```
EAR = (A + B) / (2 × C)        A = ‖p2 − p6‖   B = ‖p3 − p5‖   C = ‖p1 − p4‖
```

Se promedia la altura de dos pares y se divide por el ancho (de ahí el `2×`). Luego se **promedia el EAR de ambos ojos** para reducir ruido.

## Valores típicos

| Estado | EAR aproximado |
|---|---|
| Ojo abierto | 0.25 – 0.35 |
| Parpadeo / cierre | → 0.0 – 0.15 |
| **Umbral usado aquí** | **0.22** |

Estos valores varían por persona, cámara y ángulo ([doc 08](08-calibracion-y-limites.md)).

## Por qué un contador y no solo el umbral

Una persona despierta parpadea cada pocos segundos; cada parpadeo dura ~100–400 ms. Si alertáramos con **un solo** fotograma bajo el umbral, sonaría constantemente. La somnolencia se distingue por **cierres sostenidos**: por eso exigimos más de `N = 15` fotogramas consecutivos (0,5 s a 30 fps).

## Código

La fórmula vive en [`src/somnolencia/ear.py`](../src/somnolencia/ear.py) y tiene pruebas en [`tests/test_ear.py`](../tests/test_ear.py) (ojo abierto de valor conocido, ojo cerrado = 0, invariancia a la escala, etc.).

**Referencia:** T. Soukupová y J. Čech, *Real-Time Eye Blink Detection using Facial Landmarks*, CVWW 2016.
