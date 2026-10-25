import os
import pika


def produce(host, body):
    username = os.environ.get(
        "RABBITMQ_USER",
    )
    password = os.environ.get(
        "RABBITMQ_PASSWORD",
    )

    credentials = pika.PlainCredentials(username, password)

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host, port=5672, credentials=credentials)
    )

    try:
        channel = connection.channel()

        channel.exchange_declare(exchange="jobs", exchange_type="direct")
        channel.queue_declare(queue="router_jobs")
        channel.queue_bind(
            queue="router_jobs", exchange="jobs", routing_key="check_interfaces"
        )

        channel.basic_publish(
            exchange="jobs", routing_key="check_interfaces", body=body
        )
    finally:
        connection.close()


if __name__ == "__main__":
    host = os.environ.get("RABBITMQ_HOST", "localhost")
    produce(host, "192.168.1.44")
    print("Sent message: 192.168.1.44")
