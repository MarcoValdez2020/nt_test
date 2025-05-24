FROM python:3.12-slim

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos el archivo de requerimientos y lo instalamos
COPY requirements.txt /app/requirements.txt

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

COPY etl/app /app

CMD ["python", "main.py"]