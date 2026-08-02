from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.errores import GoldyPetSpaException
from app.clientes.rutas import router as clientes_router
from app.pets.rutas import router as pets_router

app = FastAPI(
    title="Goldy Pet Spa API",
    description="Sistema de reservas para estética canina",
    version="1.0.0"
)


@app.exception_handler(GoldyPetSpaException)
def goldy_exception_handler(request: Request, exc: GoldyPetSpaException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.message
        }
    )


app.include_router(clientes_router, prefix="/api/v1")
app.include_router(pets_router, prefix="/api/v1")


@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a Goldy Pet Spa API!"
    }