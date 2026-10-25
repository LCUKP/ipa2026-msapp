import os
import time

import pika

from callback import callback


def consume():
    host = os.environ.get("RABBITMQ_HOST", "rabbitmq")
    username = os.environ.get("RABBITMQ_USER")
    password = os.environ.get("RABBITMQ_PASSWORD")

    if not username or not password:
        raise RuntimeError("RABBITMQ_USER and RABBITMQ_PASSWORD must be set")

    connection = None

    for attempt in range(10):
        try:
            print(
                f"Connecting to RabbitMQ (try {attempt})...",
                flush=True,
            )

            credentials = pika.PlainCredentials(username, password)

            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=host,
                    port=5672,
                    credentials=credentials,
                    socket_timeout=5,
                    blocked_connection_timeout=30,
                )
            )

            print("Connected to RabbitMQ", flush=True)
            break

        except Exception as exc:
            print(
                f"RabbitMQ connection failed: {type(exc).__name__}: {exc}",
                flush=True,
            )
            time.sleep(5)

    if connection is None:
        raise RuntimeError("Could not connect to RabbitMQ after 10 attempts")

    channel = connection.channel()

    channel.exchange_declare(
        exchange="jobs",
        exchange_type="direct",
    )
    channel.queue_declare(queue="router_jobs")
    channel.queue_bind(
        queue="router_jobs",
        exchange="jobs",
        routing_key="check_interfaces",
    )
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue="router_jobs",
        on_message_callback=callback,
        auto_ack=True,
    )

    print("Waiting for router jobs...", flush=True)
    channel.start_consuming()


if __name__ == "__main__":
    consume()
