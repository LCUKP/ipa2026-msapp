import os
from datetime import datetime, timezone

from pymongo import MongoClient


def save_interface_status(router_ip, interfaces):
    mongo_uri = os.environ.get("MONGO_URI")
    db_name = os.environ.get("DB_NAME")

    if not mongo_uri or not db_name:
        raise RuntimeError("MONGO_URI and DB_NAME must be set")

    data = {
        "router_ip": router_ip,
        "timestamp": datetime.now(timezone.utc),
        "interfaces": interfaces,
    }

    with MongoClient(
        mongo_uri,
        serverSelectionTimeoutMS=5000,
    ) as client:
        db = client[db_name]
        db["interface_status"].insert_one(data)

    print(f"Stored interface status for {router_ip}", flush=True)
