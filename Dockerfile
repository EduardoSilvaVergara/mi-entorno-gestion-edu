# Imagen base: Python 3.11 versión liviana
FROM python:3.11-slim

# Evita archivos .pyc innecesarios
ENV PYTHONDONTWRITEBYTECODE=1
# Muestra los logs en tiempo real
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Primero copia solo requirements para aprovechar el caché
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Luego copia el resto del código
COPY . .

# Puerto que usa la app
EXPOSE 5000

# Comando para iniciar la app
CMD ["python", "app.py"]