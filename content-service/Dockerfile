# content-service/Dockerfile

FROM python:3.13-alpine

WORKDIR /app

# Dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sources
COPY . .

# Rendre l'entrypoint exécutable
RUN chmod +x entrypoint.sh

EXPOSE 8003

ENTRYPOINT ["./entrypoint.sh"]