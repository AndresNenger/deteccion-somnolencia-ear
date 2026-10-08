# 05 · Localización de los ojos y cálculo del EAR

**Objetivo:** pasar de 478 puntos a un único número por fotograma.

## 1. Seleccionar los 6 puntos de cada ojo

De la malla de 478 puntos solo necesitamos 12:

```python
OJO_IZQ = [33, 160, 158, 133, 153, 144]     # p1, p2, p3, p4, p5, p6
OJO_DER = [362, 385, 387, 263, 373, 380]
```

El **orden importa**: debe coincidir con `p1…p6` de la fórmula (comisura, dos puntos del párpado superior, comisura opuesta, dos puntos del párpado inferior).

## 2. Pasar a píxeles

```python
px = lm * np.array([ancho, alto])     # lm: (478, 2) normalizado → píxeles
```

**No omitas este paso.** En un video 1920×1080 una distancia horizontal de 0,01 son 19 px, pero una vertical de 0,01 son 11 px: con coordenadas normalizadas el EAR queda deformado por la relación de aspecto.

## 3. Calcular el EAR de un ojo

```python
def ear_ojo(p):
    A = np.linalg.norm(p[1] - p[5])    # vertical  p2-p6
    B = np.linalg.norm(p[2] - p[4])    # vertical  p3-p5
    C = np.linalg.norm(p[0] - p[3])    # horizontal p1-p4
    return (A + B) / (2.0 * C)
```

## 4. Promediar ambos ojos

```python
ear = (ear_ojo(px[OJO_IZQ]) + ear_ojo(px[OJO_DER])) / 2
```

Promediar reduce el ruido de un landmark mal ubicado y evita que un guiño (un ojo cerrado) dispare la alerta tan fácilmente.

## Verificación visual

Dibuja los 12 puntos sobre el primer fotograma (el notebook lo hace en el Paso 4). Deben caer sobre el contorno de los ojos; si están desplazados, el problema es la detección, no el EAR.

## En el paquete

```python
from somnolencia.ear import mean_ear
ear_promedio, ear_izq, ear_der = mean_ear(px)
```

Ver [`ear.py`](../src/somnolencia/ear.py).
