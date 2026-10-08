# 00 · Introducción y requisitos

## Qué vas a construir

Un sistema que lee un video de un conductor, localiza sus ojos fotograma a fotograma, mide qué tan abiertos están y **lanza una alerta** cuando permanecen cerrados demasiado tiempo. Produce un nuevo video anotado (`resultado.mp4`) y un CSV con el EAR de cada fotograma.

```
Video de entrada → Rostro → Ojos → EAR → ¿Somnolencia? → Video de salida con alerta
```

## Qué aprenderás

- Qué es un *landmark* facial y cómo MediaPipe obtiene 478 por rostro.
- Qué es el **Eye Aspect Ratio (EAR)** y por qué funciona.
- Cómo convertir una medida continua (EAR) en una decisión (alerta) con un umbral y un contador.
- Cómo calibrar, y por qué un solo umbral nunca sirve para todos.
- Cómo publicar y versionar el proyecto en GitHub.

## Requisitos

| Necesitas | Para qué |
|---|---|
| Cuenta de Google | Ejecutar el notebook en Google Colab (gratis, sin instalar nada) |
| Cuenta de GitHub | Publicar el repositorio ([doc 09](09-subir-a-github.md)) |
| Un video propio | Frontal, buena luz, 10–60 s. Solo con permiso de quien aparece |
| Python ≥ 3.9 *(opcional)* | Solo si quieres ejecutarlo en tu computador |

No hace falta experiencia previa en visión por computadora; sí conviene saber leer Python básico.

## Ruta de lectura

| # | Documento | Tema |
|---|---|---|
| 00 | Introducción | Este documento |
| 01 | [Teoría del EAR](01-teoria-ear.md) | La fórmula y su intuición |
| 02 | [Entorno](02-entorno-colab-y-local.md) | Colab y/o instalación local |
| 03 | [Video de entrada](03-video-de-entrada.md) | Abrir y leer fotogramas con OpenCV |
| 04 | [Rostro y landmarks](04-rostro-y-landmarks.md) | MediaPipe Face Landmarker |
| 05 | [Cálculo del EAR](05-calculo-del-ear.md) | De 6 puntos a un número |
| 06 | [Lógica de alerta](06-logica-de-alerta.md) | Umbral + contador |
| 07 | [Video de salida](07-video-de-salida.md) | Dibujar, escribir y reproducir |
| 08 | [Calibración y límites](08-calibracion-y-limites.md) | Honestidad sobre lo que no hace |
| 09 | [Subir a GitHub](09-subir-a-github.md) | Publicar el proyecto |

> ⚠️ Proyecto **educativo**. No es un sistema de seguridad vehicular ni un dispositivo certificado. Nunca confíes tu seguridad al volante a este código.
