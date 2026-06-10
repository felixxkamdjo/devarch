FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . .

RUN mkdir -p storage/images storage/videos storage/files

EXPOSE 8004

CMD ["python", "server.py"]