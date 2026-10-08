# 09 · Subir el proyecto a GitHub (paso a paso)

**Objetivo:** publicar el repositorio y dejar el botón **Abrir en Colab** funcionando.

## 1. Crear el repositorio en GitHub

1. Entra a <https://github.com/new>.
2. **Repository name:** `deteccion-somnolencia-ear`.
3. Descripción: *Detección de somnolencia en conductores con visión por computadora (EAR + MediaPipe)*.
4. Visibilidad: **Public** (necesario para que Colab abra el notebook sin autenticación).
5. **No** marques *Add a README*, *.gitignore* ni *license*: el proyecto ya los trae.
6. Pulsa **Create repository**.

## 2. Poner tu usuario en los enlaces

El proyecto usa `TU_USUARIO` como marcador en los enlaces. Reemplázalo por tu usuario de GitHub (ejemplo con `miusuario`):

```bash
# Linux / macOS / Git Bash
grep -rl "TU_USUARIO" . --exclude-dir=.git | xargs sed -i 's/TU_USUARIO/miusuario/g'
```

```powershell
# Windows PowerShell
Get-ChildItem -Recurse -File -Include *.md,*.ipynb,*.toml |
  Where-Object { $_.FullName -notmatch '\\\.git\\' } |
  ForEach-Object { (Get-Content $_.FullName -Raw) -replace 'TU_USUARIO','miusuario' | Set-Content $_.FullName -NoNewline }
```

Archivos afectados: `README.md`, `docs/02-…`, `docs/09-…` y el notebook.

## 3. Inicializar Git y hacer el primer commit

Desde la carpeta del proyecto:

```bash
git init -b main
git add .
git status          # revisa que NO aparezcan videos (*.mp4) ni models/*.task
git commit -m "Proyecto inicial: deteccion de somnolencia con EAR y MediaPipe"
```

Si Git pide identificarte la primera vez:

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu-correo@ejemplo.com"
```

## 4. Conectar y subir

```bash
git remote add origin https://github.com/miusuario/deteccion-somnolencia-ear.git
git push -u origin main
```

GitHub ya no acepta la contraseña de la cuenta por HTTPS: usa un **Personal Access Token** (*Settings → Developer settings → Personal access tokens*) o instala **GitHub CLI** (`gh auth login`). Nunca pegues un token dentro del código ni lo subas al repositorio.

## 5. Verificar

- La página del repositorio muestra el README con sus tablas y diagrama.
- La pestaña **Actions** ejecuta las pruebas (`tests`) y debe quedar en verde.
- Haz clic en **Abrir en Colab** del README: debe abrir el notebook. Si da error 404, el repositorio es privado o el usuario/rama de la URL es incorrecto.

## 6. Flujo para cambios futuros

```bash
git checkout -b ajustar-umbral          # rama para cada cambio
# ... edita ...
pytest -q                               # comprueba que nada se rompió
git add -A
git commit -m "Ajusta umbral por defecto del EAR"
git push -u origin ajustar-umbral       # abre un Pull Request desde GitHub
```

## 7. Guardar cambios hechos en Colab

En Colab: *Archivo → Guardar una copia en GitHub*. Elige el repositorio, la rama y escribe el mensaje del commit. Antes de guardar, **limpia las salidas** que incluyan imágenes de personas (*Editar → Borrar todos los resultados*).

## Qué NO subir

El `.gitignore` ya excluye `*.mp4`, `ear*.csv` y `models/*.task`. No publiques videos de terceros ni capturas con rostros identificables sin su consentimiento.
