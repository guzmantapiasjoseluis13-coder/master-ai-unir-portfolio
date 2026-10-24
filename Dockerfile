# --- ETAPA 1: Construcción de dependencias ---
FROM python:3.10-slim AS builder

WORKDIR /app

# Instalar dependencias del sistema requeridas para compilación
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias de Python en directorio de usuario
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# --- ETAPA 2: Imagen Final Optimizada ---
FROM python:3.10-slim

WORKDIR /app

# Variables de entorno para Streamlit y Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8501

# Copiar librerías instaladas desde la etapa builder
COPY --from=builder /install /usr/local

# Copiar la estructura de código fuente
COPY . /app

# Puerto expuesto para Streamlit
EXPOSE 8501

# Comprobación de estado del contenedor (Healthcheck)
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Comando de arranque del servidor
ENTRYPOINT ["streamlit", "run", "app_master_inicio.py", "--server.port=8501", "--server.address=0.0.0.0"]
