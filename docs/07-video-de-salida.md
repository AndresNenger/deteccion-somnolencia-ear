# 07 · Video de salida con alerta

**Objetivo:** dibujar la información sobre cada fotograma y guardar el resultado.

## Escribir el video

```python
writer = cv2.VideoWriter("resultado.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, (ancho, alto))
...
writer.write(frame)       # una vez por fotograma procesado
...
writer.release()          # sin esto el archivo queda corrupto
```

El tamaño `(ancho, alto)` debe coincidir exactamente con el de los fotogramas, o OpenCV descarta el video en silencio.

## Dibujar

```python
cv2.putText(frame, f"EAR: {ear:.2f}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
cv2.putText(frame, f"Contador: {contador}/{N}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
cv2.putText(frame, estado, (20, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color_estado, 2)
if estado == "SOMNOLIENTO":
    cv2.putText(frame, "ALERTA", (ancho // 2 - 110, alto // 2), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 0, 255), 5)
```

Los colores en OpenCV son **BGR**: `(0, 255, 0)` es verde, `(0, 0, 255)` es rojo.

> `cv2.putText` **no soporta tildes ni la ñ** (los dibuja como `?`). Por eso los textos del video son `DESPIERTO`, `SOMNOLIENTO`, `ALERTA`, sin acentos.

## Reproducirlo en el navegador

OpenCV escribe con el códec `mp4v`, que Chrome/Colab no reproducen. Se reconvierte con ffmpeg:

```bash
ffmpeg -y -i resultado.mp4 -vcodec libx264 -pix_fmt yuv420p resultado_h264.mp4
```

`yuv420p` es necesario para compatibilidad con navegadores y reproductores. El notebook (Paso 8) lo hace y luego incrusta el video con una etiqueta `<video>` en base64; si pesa más de 25 MB, se omite la vista previa y se ofrece la descarga.

## El CSV de resultados

Cada fila: `frame, tiempo_s, ear, contador, estado`. Sirve para graficar el EAR contra el umbral y para calibrar ([doc 08](08-calibracion-y-limites.md)):

```python
df = pd.read_csv("ear.csv")
df.plot(x="tiempo_s", y="ear")
```

## Desde el paquete

```python
from somnolencia.pipeline import process_video

resumen = process_video("entrada.mp4", "resultado.mp4", csv_path="ear.csv")
print(resumen["eventos_alerta"], "alertas")
```
