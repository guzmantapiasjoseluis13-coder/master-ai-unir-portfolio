# ETAPA 1: Builder (Compilación de dependencias)
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Instalar herramientas de compilación (necesarias para algunas librerías)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Crear wheels o entorno virtual independiente
RUN python -m pip install --upgrade pip \
    && pip install --user -r requirements.txt

# ETAPA 2: Runtime (Imagen final ligera)
FROM python:3.12-slim AS runtime

WORKDIR /app

# Copiar las dependencias instaladas desde la etapa builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copiar el código fuente
COPY . .

# Exponer el puerto del backend (FastAPI)
EXPOSE 8000

# Comando por defecto
CMD ["uvicorn", "tfm.backend_api.main:app", "--host", "0.0.0.0", "--port", "8000"]