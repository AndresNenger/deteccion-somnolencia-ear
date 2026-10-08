# 08 · Calibración, límites y seguridad

**Objetivo:** saber cuándo confiar en el resultado y cuándo no.

## Calibrar el umbral

0.22 es un **valor inicial razonable**, no una constante física. Procedimiento:

1. Procesa un video del conductor **despierto** y grafica el EAR (celda de análisis del notebook).
2. Mira el nivel con ojos abiertos (la "línea base") y el de los parpadeos.
3. Fija el umbral aproximadamente al **70–80 % de la línea base**, de modo que ojos abiertos queden claramente por encima y los cierres por debajo.
4. Repite con un video con cierres prolongados reales o simulados y comprueba que alerta.

Un ejemplo real durante el desarrollo: una foto frontal de prueba de MediaPipe dio **EAR = 0.211**, por debajo del umbral por defecto, aunque la persona no dormía. Una persona con ojos naturalmente entrecerrados o mirando hacia abajo produce falsos positivos con 0.22; de ahí la calibración por persona.

## Qué degrada el resultado

| Factor | Efecto |
|---|---|
| Cabeza girada o inclinada | EAR bajo falso (el ojo se ve más estrecho) |
| Mirar hacia abajo (celular, tablero) | EAR bajo sin que haya somnolencia |
| Gafas (reflejos, montura gruesa) o gafas de sol | Landmarks inestables o ausentes |
| Poca luz / contraluz | Rostro no detectado |
| Cámara muy lejana o baja resolución | Ruido en los puntos |
| Fotogramas por segundo bajos | El contador representa más tiempo |

## Qué NO mide

- El EAR mide **cierre ocular**, no somnolencia. Hay microsueños con ojos medio abiertos y personas que cierran los ojos por otros motivos.
- No detecta bostezos, cabeceo, desviación del carril ni tiempo de reacción.
- Con varias personas en el cuadro, solo se analiza **una cara** (`num_faces=1`).
- La evaluación de este proyecto es cualitativa: **no se ha medido** sensibilidad/especificidad con un conjunto de datos etiquetado.

## Ideas de extensión

- **PERCLOS:** porcentaje de tiempo con ojos cerrados en una ventana (p. ej. 60 s); es la métrica más usada en la literatura.
- **MAR** (*Mouth Aspect Ratio*) para bostezos.
- **Pose de cabeza** (cabeceo) con los landmarks y `cv2.solvePnP`.
- Calibración automática de la línea base durante los primeros segundos.
- Alerta sonora (en local, con `winsound` o `playsound`).
- Evaluar con un conjunto etiquetado como NTHU-DDD o YawDD y reportar métricas.

## ⚠️ Seguridad y alcance

- **No es un dispositivo médico ni de seguridad vehicular.** No uses este código para decidir si es seguro conducir.
- Si te sientes somnoliento al volante: **detente y descansa**. Ninguna alerta de software sustituye eso.
- **Privacidad:** procesar rostros es tratar datos biométricos. Usa solo videos propios o con consentimiento explícito, y no subas a GitHub videos de otras personas (el `.gitignore` ya excluye `*.mp4`).
