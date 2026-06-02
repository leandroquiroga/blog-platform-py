# Blogging Platform API

API RESTful para una plataforma de blogs construida con FastAPI, MongoDB (Beanie ODM), Redis como caché y autenticación JWT.

Este proyecto forma parte de los [Roadmap.sh](https://roadmap.sh/projects/blogging-platform-api) — diseñado como un ejercicio práctico de aprendizaje sobre arquitectura backend con Python.

## Características

- **Operaciones CRUD** para posts de blog (Crear, Leer, Actualizar, Eliminar)
- **MongoDB** con Beanie ODM para manejo asíncrono de documentos
- **Caché con Redis** usando patrón Cache-Aside (TTL de 5 minutos, invalidación automática en escrituras)
- **Autenticación JWT** (HS256, tokens de 30 minutos) con hashing de contraseñas bcrypt
- **Registro e inicio de sesión** de usuarios con email y contraseña
- **Propiedad de posts** — solo los autores pueden modificar o eliminar sus posts
- **Rate limiting** vía Redis (ventana fija, configurable, basado en middleware)
- **Perfil de usuario** (`GET /me`) que devuelve datos del usuario + sus posts

## Stack Tecnológico

| Capa | Tecnología |
|------|-----------|
| Framework | FastAPI (Python asíncrono) |
| Base de datos | MongoDB 7 (vía Beanie ODM) |
| Caché | Redis 7 (asíncrono) |
| Autenticación | JWT (python-jose) + bcrypt (passlib) |
| Validación | Pydantic v2 |
| Infraestructura | Docker Compose |

## Estructura del Proyecto

```
app/
├── config/
│   ├── setting_config.py     # Variables de entorno (pydantic-settings)
│   ├── database_config.py    # Conexión a MongoDB + init Beanie
│   └── redis_config.py       # Gestión de conexión a Redis
├── models/
│   ├── blog_models.py        # BlogModel (Documento Beanie)
│   └── user_models.py        # UserModel (Documento Beanie)
├── schemas/
│   ├── blog_schema.py        # PostCreateSchema, PostResponseSchema
│   └── user_schema.py        # UserCreateSchema, UserResponseSchema, LoginSchema, TokenSchema
├── repositories/
│   ├── blog_repository.py    # Acceso a datos de blogs (consultas Beanie)
│   └── user_repository.py    # Acceso a datos de usuarios
├── services/
│   ├── blog_service.py       # Lógica de negocio de blogs + orquestación de caché
│   └── auth_services.py      # Lógica de autenticación (registro, login, JWT)
├── routes/
│   ├── blog_routes.py        # Endpoints /api/v1/posts
│   └── auth_routes.py        # Endpoints /auth
├── middlewares/
│   └── rate_limit_middleware.py  # Rate limiting con Redis
├── utils/
│   ├── cache_utils.py        # Helpers de caché Redis
│   ├── secutiry_utils.py     # Hashing de contraseñas + JWT
│   └── validation_utils.py   # Tipo personalizado PyObjectId
├── dependencies.py           # Inyección de dependencias FastAPI
└── main.py                   # App FastAPI, lifespan, registro de rutas
```

## Cómo Empezar

### Requisitos

- Python 3.12+
- Docker (para MongoDB y Redis)

### Instalación

1. Clonar el repositorio:
   ```bash
   git clone <repo-url>
   cd blogging-platform-py
   ```

2. Crear un entorno virtual e instalar dependencias:
   ```bash
   python -m venv venv
   source venv/bin/activate  # o `venv\Scripts\activate` en Windows
   pip install -r requirements.txt
   ```

3. Iniciar MongoDB y Redis con Docker:
   ```bash
   docker compose up -d
   ```

4. Configurar variables de entorno (el `.env` ya viene preconfigurado para desarrollo local):
   ```
   DATABASE_NAME=blog_py
   URL_MONGO_DB=mongodb://localhost:27017/blog_py
   REDIS_HOST=localhost
   REDIS_PORT=6379
   REDIS_DB=0
   JWT_SECRET_KEY=<tu-clave-secreta>
   JWT_ALGORITHM=HS256
   JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
   RATE_LIMIT=10/minute
   ```

5. Ejecutar la aplicación:
   ```bash
   python run.py
   ```

   API disponible en `http://localhost:8000`. Documentación interactiva en `http://localhost:8000/docs`.

## Endpoints de la API

### Autenticación (`/auth`)

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|:----:|
| POST | `/auth/register` | Registrar un nuevo usuario | No |
| POST | `/auth/login` | Iniciar sesión, devuelve token JWT | No |
| GET | `/auth/me` | Obtener usuario actual + sus posts | Sí |

### Posts (`/api/v1/posts`)

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|:----:|
| GET | `/api/v1/posts` | Listar todos los posts (`?term=` búsqueda opcional) | No |
| GET | `/api/v1/posts/{id}` | Obtener un post por ID | No |
| POST | `/api/v1/posts` | Crear un nuevo post | Sí |
| PUT | `/api/v1/posts/{id}` | Actualizar un post (solo el autor) | Sí |
| DELETE | `/api/v1/posts/{id}` | Eliminar un post (solo el autor) | Sí |

### Flujo de Autenticación

1. `POST /auth/register` con `{ "username": "...", "email": "...", "password": "..." }`
2. `POST /auth/login` con `{ "email": "...", "password": "..." }` → recibís `access_token`
3. Incluir header `Authorization: Bearer <token>` en los endpoints protegidos

### Rate Limiting

Por defecto: **10 peticiones por minuto** por IP del cliente (configurable vía `RATE_LIMIT` en `.env`). Al exceder el límite, la API devuelve `429 Too Many Requests` con header `Retry-After` y headers informativos `X-RateLimit-*`.

## Decisiones de Diseño Clave

- **Arquitectura por capas** (routes → services → repositories → models) para separación de responsabilidades
- **Beanie ODM** en lugar de PyMongo puro — nativamente asíncrono, compatible con Pydantic, elimina boilerplate
- **Patrón Cache-Aside** — lógica de caché explícita en la capa de servicios, sin decoradores mágicos
- **FastAPI lifespan** para orden garantizado de inicio/cierre (vs `@app.on_event` deprecado)
- **Separación DTO** — `CreateSchema` para entrada, `ResponseSchema` para salida (nunca exponer campos internos)
- **`@property` en Settings** — parseo del string `"10/minute"` a valores numéricos reutilizables

---

> Este proyecto fue construido como parte del desafío [Blogging Platform API](https://roadmap.sh/projects/blogging-platform-api) de [Roadmap.sh](https://roadmap.sh).
