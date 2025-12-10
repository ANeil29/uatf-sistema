FROM python:3.12-slim

# 1. INSTALA LAS LIBRERÍAS DEL SISTEMA QUE FALTAN (ESTO ES LO MÁS IMPORTANTE)
RUN apt-get update && apt-get install -y \
    libcairo2-dev \
    libpango1.0-dev \
    libgdk-pixbuf2.0-dev \
    libffi-dev \
    shared-mime-info \
    pkg-config \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 2. Prepara el entorno de trabajo
WORKDIR /app
ENV PYTHONUNBUFFERED=1

# 3. Copia e instala las dependencias de Python
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 4. Copia el resto del código de tu proyecto
COPY . .

# 5. Define el comando para iniciar tu app (REEMPLAZA 'tu_proyecto' con el nombre real)
CMD ["gunicorn", "uatf-SISTEMA.wsgi:application", "--bind", "0.0.0.0:$PORT"]