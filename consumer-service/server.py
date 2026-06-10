# consumer-service/server.py

import os
import json
import time
import pika


RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.environ.get("RABBITMQ_USER", "devarch")
RABBITMQ_PASS = os.environ.get("RABBITMQ_PASS", "devarch123")

QUEUES = [
    "article.published",
]


def on_article_published(ch, method, properties, body):
    """Traite un event article.published."""
    
    try:
        payload = json.loads(body)
        
        print(
            f"[consumer] - article.published - "
            f"id={payload.get('article_id')} | "
            f"title='{payload.get('title')}' | "
            f"author='{payload.get('author_name')}'",
            flush=True
        )
        # ACK - on confirme la reception du message
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"[consumer] ERROR processing message: {e}", flush=True)
        # NACK - remet le message en queue
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


HANDLERS = {
    "article.published": on_article_published,
}


def connect_with_retry(max_attempts=10, delay=3):
    """Tente de se connecter à RabbitMQ avec retry."""
    
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    
    params      = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        credentials=credentials,
        heartbeat=60
    )

    for attempt in range(1, max_attempts + 1):
        try:
            print(f"[consumer] Connecting to RabbitMQ ({attempt}/{max_attempts})…", flush=True)
            conn = pika.BlockingConnection(params)
            print("[consumer] Connected.", flush=True)
            return conn
        except Exception as e:
            print(f"[consumer] Connection failed: {e}", flush=True)
            if attempt < max_attempts:
                time.sleep(delay)

    raise RuntimeError("Could not connect to RabbitMQ after multiple attempts.")


def run():
    connection = connect_with_retry()
    channel    = connection.channel()

    # Déclare toutes les queues écoutées
    for queue in QUEUES:
        channel.queue_declare(queue=queue, durable=True)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(
            queue=queue,
            on_message_callback=HANDLERS[queue]
        )
        print(f"[consumer] Listening on queue '{queue}'", flush=True)

    print("[consumer] Waiting for messages. CTRL+C to stop.", flush=True)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    finally:
        connection.close()


if __name__ == "__main__":
    run()