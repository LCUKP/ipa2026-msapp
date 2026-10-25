import os

from pymongo import MongoClient


def get_router_info():
    mongo_uri = os.environ.get("MONGO_URI")
    db_name = os.environ.get("DB_NAME")

    if not mongo_uri or not db_name:
        raise RuntimeError("MONGO_URI and DB_NAME must be set")

    with MongoClient(mongo_uri, serverSelectionTimeoutMS=5000) as client:
        db = client[db_name]
        routers = db["routers"]
        return list(routers.find())


if __name__ == "__main__":
    for data in get_router_info():
        safe_data = dict(data)
        if "password" in safe_data:
            safe_data["password"] = "<redacted>"
        print(safe_data)
