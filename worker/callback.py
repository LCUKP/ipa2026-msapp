from bson import json_util

from database import save_interface_status
from router_client import get_interfaces


def callback(channel, method, properties, body):
    router_ip = "unknown"

    try:
        job = json_util.loads(body.decode("utf-8"))

        router_ip = job["ip"]
        username = job["username"]
        password = job["password"]

        print(f"Received job for router {router_ip}", flush=True)

        interfaces = get_interfaces(router_ip, username, password)
        save_interface_status(router_ip, interfaces)

    except Exception as exc:
        print(
            f"Error processing router {router_ip}: " f"{type(exc).__name__}: {exc}",
            flush=True,
        )
