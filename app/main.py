from fastapi import FastAPI

app = FastAPI(
    title="Goldy Pet Spa API",
    description="Sistema de reservas para estética canina",
    version="1.0.0"
)

@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a Goldy Pet Spa API!"
    }   