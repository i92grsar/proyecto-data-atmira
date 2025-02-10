# Usar una imagen base de Python (puedes ajustar la versión si lo deseas)
FROM python:3.9-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo de dependencias y luego instalarlo
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar todo el proyecto al contenedor
COPY . .

# Comando por defecto para ejecutar el pipeline
CMD ["python", "scripts/pipeline.py"]
