# 1. Usar una imagen base oficial de Python
FROM python:3.13-slim

# 2. Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiar el archivo de requerimientos e instalarlos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiar el resto del código de la aplicación
COPY api.py .

# 5. Exponer el puerto en el que correrá la aplicación
EXPOSE 80

# 6. Comando para ejecutar la aplicación al iniciar el contenedor
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "80"]