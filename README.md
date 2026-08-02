# Goldy Pet Spa API

API REST desarrollada con FastAPI para la administración de clientes y mascotas de una estética canina.

## Requisitos

* Docker Desktop
* Git

## Instalación

1. Clonar el repositorio.

```bash
git clone https://github.com/Ere8712/goldy-pet-spa-api.git
```

2. Entrar a la carpeta del proyecto.

```bash
cd goldy-pet-spa-api
```

3. Crear el archivo `.env` tomando como base el archivo `.env.example`.

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

Construir e iniciar los contenedores:

```bash
docker compose up --build
```

O ejecutarlos en segundo plano:

```bash
docker compose up -d --build
```

## Documentación

Una vez iniciado el proyecto, la documentación interactiva estará disponible en:

```
http://localhost:8000/docs
```

## Tecnologías utilizadas

* FastAPI
* SQLAlchemy
* PostgreSQL
* Alembic
* Docker
* Docker Compose
* Pydantic
