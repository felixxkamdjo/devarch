# content-service/events/publisher.py

import os
import json
import pika

RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.environ.get("RABBITMQ_USER", "devarch")
RABBITMQ_PASS = os.environ.get("RABBITMQ_PASS", "devarch123")


def _get_connection():

    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)

    params = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        credentials=credentials,
        connection_attempts=3,
        retry_delay=2,
    )

    return pika.BlockingConnection(params)


def publish(queue: str, payload: dict):
    """
    Publie un message JSON dans la queue spécifiée.
    Silencieux en cas d'erreur — RabbitMQ est optionnel.
    """

    try:
        connection = _get_connection()
        channel = connection.channel()

        # Déclare la queue (idempotent - créée si elle n'existe pas)
        channel.queue_declare(queue=queue, durable=True)

        channel.basic_publish(
            exchange="",
            routing_key=queue,
            body=json.dumps(payload),
            properties=pika.BasicProperties(
                delivery_mode=2, content_type="application/json"  # message persistant
            ),
        )

        connection.close()
        print(f"[publisher] - {queue} : {payload}", flush=True)

    except Exception as e:
        # RabbitMQ non dispo - on logue sans planter
        print(f"[publisher] WARNING — could not publish to {queue}: {e}", flush=True)
