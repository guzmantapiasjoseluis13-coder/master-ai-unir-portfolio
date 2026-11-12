from fastapi import FastAPI

app = FastAPI(
    title="Master AI Portfolio API",
    version="1.0.0",
    description="API Gateway para microservicios de Inteligencia Artificial"
)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Backend FastAPI operativo"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
