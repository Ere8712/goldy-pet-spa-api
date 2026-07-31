from fastapi import FastAPI

app = FastAPI(
    title="Goldy Pet Spa API",
    version="1.0.0"
)

@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a Goldy Pet Spa API!"
    }   