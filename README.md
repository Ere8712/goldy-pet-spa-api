# Goldy Pet Spa API

API REST desarrollada con **FastAPI** para la administración de clientes y mascotas de una estética canina.

## Tecnologías utilizadas

* Python 3.12
* FastAPI
* SQLAlchemy
* Alembic
* PostgreSQL
* Docker
* Docker Compose
* Pydantic

## Características

* API REST con FastAPI.
* Base de datos PostgreSQL.
* ORM mediante SQLAlchemy.
* Migraciones con Alembic.
* Configuración mediante variables de entorno.
* Contenerización con Docker.
* Documentación automática con Swagger.

## Estructura del proyecto

```text
goldy-pet-spa-api/
│
├── alembic/
├── app/
│   ├── clientes/
│   ├── pets/
│   ├── database.py
│   ├── errores.py
│   └── main.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── alembic.ini
├── .env.example
└── README.md
```

## Configuración

Crear un archivo `.env` tomando como base `.env.example`.

Ejemplo:

```env
COMPOSE_PROJECT_NAME=goldypetspa

POSTGRES_USER=goldy_user
POSTGRES_PASSWORD=goldy_password
POSTGRES_DB=GoldyPetSpa

DATABASE_URL=postgresql://goldy_user:goldy_password@db:5432/GoldyPetSpa

APP_NAME=Goldy Pet Spa API
ENVIRONMENT=development
```

## Ejecución

Construir y levantar el proyecto:

```bash
docker compose up --build
```

Para ejecutar en segundo plano:

```bash
docker compose up -d --build
```

## Documentación

Una vez iniciado el proyecto, la documentación interactiva está disponible en:

```
http://localhost:8000/docs
```

## Migraciones

Crear una migración:

```bash
alembic revision --autogenerate -m "descripcion"
```

Aplicar migraciones:

```bash
alembic upgrade head
```

## Módulos implementados

### Clientes

CRUD completo:

* Crear cliente
* Listar clientes
* Consultar cliente por ID
* Actualizar cliente (PUT)
* Actualización parcial (PATCH)
* Eliminar cliente

### Pets

CRUD completo:

* Crear mascota
* Listar mascotas
* Consultar mascota por ID
* Actualizar mascota (PUT)
* Actualización parcial (PATCH)
* Eliminar mascota

## Estado del proyecto

**Avance práctico 1 completado.**

Incluye:

* FastAPI
* SQLAlchemy
* Alembic
* Docker y Docker Compose
* Variables de entorno
* CRUD completo de Clientes
* CRUD completo de Pets
* Esquemas Pydantic
* Documentación Swagger
* Proyecto organizado por módulos
