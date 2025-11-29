# 🎵 Player API – Melodía

Microservicio **Player API** encargado del **manejo de audio**, incluyendo **subida de pistas**, generación de **URLs públicas y URLs firmadas**, validación de autenticación vía **JWT**, y endpoints básicos de salud y debugging.

* 🧠 Construido con **FastAPI (Python 3.13)**
* ☁️ Integrado con **Supabase Storage + Postgres**
* 🔐 Autenticación mediante **JWT Middleware**
* 🚀 Preparado para despliegue con **Docker + GitHub Actions + EC2**

Este servicio funciona como el **punto único de acceso** para manipular archivos de audio del ecosistema Melodía: subida, acceso temporal, metadatos y validaciones.

## 🧭 Índice

1. [Contexto y propósito](#-contexto-y-propósito)
2. [Features principales (Highlights)](#-features-principales-highlights)
3. [Stack tecnológico y bibliotecas clave](#-stack-tecnológico-y-bibliotecas-clave)
4. [Arquitectura interna](#-arquitectura-interna)
5. [Base de datos y Supabase Storage](#-base-de-datos-y-supabase-storage)
6. [Manejo de archivos y URLs firmadas](#-manejo-de-archivos-y-urls-firmadas)
7. [Autenticación JWT](#-autenticación-jwt)
8. [Guía para desarrolladores](#-guía-para-desarrolladores)
9. [Validaciones, tests y coverage](#-validaciones-tests-y-coverage)
10. [CI/CD y despliegue](#-cicd-y-despliegue)
11. [Referencia rápida de endpoints](#-referencia-rápida-de-endpoints)
12. [Healthcheck y debugging](#-healthcheck-y-debugging)

## 🧠 Contexto y Propósito

**Player API** centraliza toda la lógica vinculada a **gestión de pistas** dentro del ecosistema Melodía.

### Este servicio permite:

> 🎶 Subir archivos de audio a Supabase Storage, generar URLs temporales/públicas y exponer endpoints para consumo seguro por parte de otros microservicios y la app móvil.

### Responsabilidades clave:

* Subida de archivos de audio (`mp3`, `wav`, etc.)
* Obtención de URLs públicas o firmadas con expiración.
* Validación de permisos mediante JWT.
* Manejo de metadatos asociados (nombre, path, user, timestamps).
* Interfaz limpia para que otros servicios consuman pistas sin conocer detalles de Supabase.

## 🌟 Features principales (Highlights)

* 🎧 **Subida de pistas de audio**

  * Permite almacenar audios en buckets administrados por Supabase Storage.
  * Normalización de nombres y carpetas.

* 🔗 **Generación de URLs firmadas**

  * URLs temporales (firmadas) para acceso seguro.
  * URLs públicas cuando corresponde (para ciertos assets).

* 🔐 **Middleware JWT**

  * Autenticación obligatoria.
  * Rechazo automático de tokens inválidos o expirados.

* 🗄️ **Persistencia de metadatos**

  * Guarda datos relevantes en Postgres mediante Supabase.

* 🩺 **Healthcheck y logs estructurados**

  * Endpoint `/health` y logging central a través de `logger.py`.

## ⚙️ Stack Tecnológico y bibliotecas clave

### 🧱 Stack principal

* **FastAPI + Pydantic v2**
  Framework moderno y rápido, ideal para microservicios I/O–bound.

* **Supabase Python SDK**
  Acceso a:

  * PostgREST (consultas a Postgres)
  * Storage (upload, signed URLs)

* **Python 3.13**

* **Docker + Docker Compose**
  Entornos reproducibles en desarrollo y producción.

* **pytest + pytest-cov**

### 📚 Bibliotecas principales

* `fastapi`, `uvicorn`
* `pydantic`
* `supabase-py`
* `python-jose` o equivalente para **JWT**
* `pytest`, `pytest-cov`

## 🏗️ Arquitectura interna

Estructura del proyecto:

```

src/
  main.py                 # Inicialización FastAPI + middlewares + routers
  config.py               # Variables de entorno y settings
  middleware/
    auth_middleware.py    # Validación JWT para todos los endpoints protegidos
  controllers/
    player_controller.py  # Endpoints /player/*
  repositories/
    storage_repository.py # Operaciones con Supabase Storage
    db_repository.py      # Persistencia de metadatos
  utils/
    file_utils.py         # Normalización, validación, extensiones permitidas
resources/
  logger.py               # Logging estructurado
tests/
  ...

```

### Flujo interno típico

1. Cliente → `POST /player/upload`.
2. Middleware valida JWT.
3. Controller recibe archivo y metadata.
4. Repositorio lo almacena en Supabase Storage.
5. Se guardan metadatos en Postgres.
6. Se responde con URL pública o firmada.

## 🗄️ Base de datos y Supabase Storage

### Base de datos (Postgres vía Supabase)

Se utiliza para:

* Registrar metadatos de pistas.
* Asociar usuario ↔ archivo.
* Guardar timestamps, paths y estados.

### Supabase Storage

Utilizado para almacenar los archivos de audio.

Buckets típicos:

```

audio/
  raw/
  processed/

```

### Variables de entorno relevantes

```env

SUPABASE_URL=https://<proyecto>.supabase.co
SUPABASE_SERVICE_ROLE_KEY=<key>
SUPABASE_BUCKET=audio

```

## 🔥 Manejo de archivos y URLs firmadas

### Subida de archivos

* Validación de extensión.
* Normalización de nombre (`uuid` + extensión).
* Guardado en el bucket configurado.

### URLs firmadas

* Duración configurable (ej: 60s, 5min).
* Se genera via Supabase Storage.

Ejemplo:

```python

supabase.storage.from_(bucket).create_signed_url(path, expires_in=60)

```

## 🔐 Autenticación JWT

Toda ruta protegida pasa por `auth_middleware.py`, que:

* Extrae `Authorization: Bearer <token>`.
* Decodifica y valida.
* Inyecta información del usuario en el request.
* Retorna **401** si el token es inválido, malformado o expirado.

Variables:

```env

JWT_SECRET=<secret>
JWT_ALGORITHM=HS256

```

## 👩‍💻 Guía para desarrolladores

### Requisitos previos

* Docker + Docker Compose
* Python 3.13 (si se ejecuta local sin Docker)
* Archivo `.env` configurado
* Credenciales Supabase

### 🚀 Arranque rápido

#### Opción A — con Make (recomendado)

```bash

make up
make test
make down

```

#### Opción B — Docker Compose directo

```bash

docker compose up -d --build
docker compose logs -f player-api
docker compose down

```

### 🌍 Variables de entorno (ejemplo)

```env

APP_ENV=development
ALLOWED_ORIGINS=*
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=xxx
SUPABASE_BUCKET=audio
JWT_SECRET=xxxx
JWT_ALGORITHM=HS256
LOG_LEVEL=INFO

```

## 🧪 Validaciones, tests y coverage

### Tests automatizados

Ejemplo:

```bash

pytest --cov=src --cov-report=xml tests/ -v

```

Se testean:

* Validación JWT
* Subida de archivos (mock Storage)
* Generación de URLs firmadas
* Endpoints `/health` y flujo básico

### Cobertura mínima

Como en el resto del ecosistema:

```bash

pytest --cov=src --cov-fail-under=75

```

### Linter (si está configurado)

```bash

ruff check src tests
# o flake8

```

---

## 🔁 CI/CD y despliegue

### 🧪 CI — GitHub Actions

Workflow típico:

1. Instalación de dependencias
2. Ejecución de tests + coverage
3. Validación de coverage ≥ 75%
4. Linting opcional

### 🚀 CD — Deploy automatizado en EC2

Mediante runner self-hosted:

1. Build & Push → Docker Hub (`jandresen99/player-api:latest`)
2. Pull en EC2
3. Reemplazo del contenedor
4. Carga de `.env` productivo
5. Limpieza de contenedores viejos

## 📡 Referencia rápida de endpoints

| Método | Ruta                 | Descripción                           |
| ------ | -------------------- | ------------------------------------- |
| `GET`  | `/health`            | Verifica que el servicio esté activo. |
| `POST` | `/player/upload`     | Sube un archivo de audio.             |
| `GET`  | `/player/signed-url` | Devuelve URL firmada para un archivo. |
| `GET`  | `/player/public-url` | Devuelve URL pública (si aplica).     |

### 📨 Ejemplo — Subir archivo

```bash

curl -X POST http://localhost:8082/player/upload \
  -H "Authorization: Bearer <JWT>" \
  -F "file=@song.mp3"

```

Respuesta típica:

```json

{
  "path": "audio/raw/uuid123.mp3",
  "signed_url": "https://..."
}

```

## 🩺 Healthcheck y debugging

### 🔍 Healthcheck básico

```bash

curl -I http://localhost:8082/health
# HTTP/1.1 200 OK

```

### 📝 Logs estructurados

Centralizados en `resources/logger.py`, integrados con Uvicorn.
