FROM python:3.12-slim

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos el archivo de requerimientos y lo instalamos
COPY requirements.txt /app/requirements.txt

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

COPY api/app /app

# Exponemos el puerto 8000
EXPOSE 8000
# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]