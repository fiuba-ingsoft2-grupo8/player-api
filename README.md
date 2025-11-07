# Player API

Microservicio **Player API** para manejo de pistas (upload y obtención de URLs públicas/firmadas) y endpoints de salud.  
Construido con **FastAPI (Python 3.13)** y **Supabase** (PostgreSQL + Storage).  
Incluye autenticación por **JWT** (middleware), logging centralizado y **tests con coverage** en CI.

 

## Elección del Stack

- **FastAPI + Pydantic v2**: tipado fuerte, validación declarativa y auto-docs (OpenAPI/Swagger). Ideal para microservicios I/O–bound.
- **Supabase Python SDK**: acceso directo a **Postgres** (PostgREST) y **Storage** (buckets) con URLs firmadas.
- **Uvicorn**: servidor ASGI rápido y simple para prod.
- **Docker + Compose + Make**: entorno reproducible con comandos cortos y red compartida con otros servicios.
- **CI (GitHub Actions) + pytest + pytest-cov**: suite de tests que impone **coverage ≥ 75%** (thresholdAll: 0.75) y genera `coverage.xml`.
- **Logging estructurado**: configuración central (uvicorn, root logger) vía `resources/logger.py`.

 

## Requisitos Previos

- **Docker** y **Docker Compose**
- **Make** (opcional, recomendado)
- **Python 3.13** (solo si querés correr sin Docker)

 

## 📍 Rutas Principales

- Salud: `GET /health` → `{}` (200)
- Player:
  - `POST /player/tracks/upload` → Sube un audio a **Supabase Storage** (bucket `PLAYER_BUCKET`, default `tracks`) y devuelve metadatos + `public_url`.
  - `GET /player/tracks/{track_id}` → Devuelve `{"url": "<public_url>"}` para la pista.

> La API expone CORS según `ALLOWED_ORIGINS`.

### Ejemplos

**Health**
```bash
curl -sS http://localhost:8082/health
# {}
```

**Obtener URL pública**
```bash
curl -sS http://localhost:8082/player/tracks/12345
# {"url":"https://.../tracks/12345.mp3"}
```

**Subir pista** (multipart/form-data)
```bash
curl -sS -X POST http://localhost:8082/player/tracks/upload   -H "Authorization: Bearer <JWT>"   -F "file=@./song.mp3"
```

> El upload espera un `UploadFile` y resuelve `mime_type` automáticamente (vía `mimetypes`).  
> El servicio retorna: `id`, `audio_path`, `mime_type`, `public_url`.

## 🔐 Autenticación

El servicio incluye dependencia `verify_token` basada en **HS256** (`JWT_SECRET`).  
En **tests** se desactiva automáticamente (flag `is_testing()`).

Variables relevantes:
- `JWT_SECRET` (obligatoria en entornos reales)

## 🚀 Inicio Rápido con Docker

### Opción A — **Make** (recomendado)

```bash
# Construir imagen y levantar API
make up

# Ejecutar tests + coverage local
make test

# Bajar entorno
make down
```

Esto:
- Construye `player-api:latest`
- Expone `http://localhost:8082`
- Inyecta envs a partir del `.env`/entorno
- Usa la red `melodia-network` (bridge)

### Opción B — **Docker Compose** directo

```bash
# Build + Up
docker compose up -d --build

# Logs
docker compose logs -f player-api

# Down
docker compose down
```

**Puertos**
- Host `8082` → Contenedor `8080` (ver `docker-compose.yml`)

## 🔧 Configuración

Variables de entorno (ver **`.env.example`**):

```env
# FastAPI
APP_ENV=development
ALLOWED_ORIGINS=*

# Supabase
SUPABASE_URL=https://<tu-proyecto>.supabase.co
SUPABASE_SERVICE_ROLE_KEY=<service_role_key>

# Buckets / TTL de URLs firmadas
AUDIO_BUCKET=audio
IMAGES_BUCKET=images
SIGNED_URL_TTL=3600
PLAYER_BUCKET=tracks

# Auth
JWT_SECRET="secret"
```

> **Importante:** La **Service Role Key** es **solo backend**.

## ⚙️ Desarrollo sin Docker

```bash
# (opcional) crear venv
python -m venv .venv && source .venv/bin/activate

# deps runtime + test
pip install -r requirements.txt
pip install -r requirements-tests.txt

# run
python src/main.py
# → http://localhost:8080

# tests + coverage
pytest --cov=src --cov-report=xml tests/test_main.py -v
```

## 🧩 Estructura del Proyecto

```
src/
  main.py                   # app FastAPI, CORS, routers, /health
  auth.py                   # verificación JWT (HS256)
  config.py                 # Settings (Pydantic) desde env
  repositories.py           # acceso Postgres vía Supabase (artists/albums/tracks)
  supabase_client.py        # factory Supabase Client
  utils.py                  # firmas de URL y helpers
  resources/logger.py       # logging config
  controllers/player_controller.py   # rutas /player/...
tests/
  conftest.py               # TestClient + mocks Supabase
  test_main.py              # tests de /health
```

> En tests se **mockea** el SDK de Supabase para aislar la lógica y acelerar.

## 🩺 Health & Debug

**API responde**
```bash
curl -I http://localhost:8082/health
# HTTP/1.1 200 OK
```

**Variables cargadas (rápido)**
```bash
docker compose exec player-api env | egrep 'APP_ENV|SUPABASE|BUCKET|JWT'
```

**Errores comunes**
- 401/403: revisar `Authorization: Bearer <JWT>` y `JWT_SECRET`.
- 5xx en upload: chequear `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY` y bucket `PLAYER_BUCKET`.

## 🧰 Makefile (objetivos)

```makefile
build-system:   # build de la imagen
up:             # compose up -d --build
down:           # compose down
test:           # pytest --cov=src --cov-report=xml tests/test_main.py -v
```

## 🔁 CI/CD

### CI — Coverage en PRs y main
Workflow: `.github/workflows/test.yaml`

- Instala `requirements.txt` + `requirements-tests.txt`
- Ejecuta: `pytest --cov=src --cov-report=xml tests/test_main.py -v`
- Publica cobertura y valida **umbral ≥ 75%**

### CD — Deploy en EC2 con Docker
Workflow: `.github/workflows/deploy.yaml`

- Build & Push a Docker Hub (`jandresen99/player-api:latest`)
- En runner self-hosted:
  - limpia contenedores/volúmenes viejos
  - descarga imagen
  - ejecuta contenedor con envs productivos (secrets)

## 📚 OpenAPI / Swagger

Una vez levantado:
- Swagger UI: `http://localhost:8082/docs`
- OpenAPI JSON: `http://localhost:8082/openapi.json`
