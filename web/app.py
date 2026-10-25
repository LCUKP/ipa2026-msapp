import os

from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson import ObjectId
from bson.errors import InvalidId

app = Flask(__name__)

mongo_uri = os.environ.get("MONGO_URI")
db_name = os.environ.get("DB_NAME")

if not mongo_uri or not db_name:
    raise RuntimeError("MONGO_URI and DB_NAME must be set")

client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
db = client[db_name]
router_collection = db["routers"]


@app.route("/")
def index():
    try:
        routers = list(router_collection.find({}, {"password": 0}).sort("_id", -1))
        return render_template("index.html", routers=routers, error=None)
    except PyMongoError:
        return (
            render_template(
                "index.html",
                routers=[],
                error="Cannot connect to MongoDB. Check the Mongo container.",
            ),
            503,
        )


@app.route("/router/<router_ip>")
def router_detail(router_ip):
    try:
        records = list(
            db["interface_status"]
            .find(
                {"router_ip": router_ip},
                {"_id": 0, "router_ip": 1, "timestamp": 1, "interfaces": 1},
            )
            .sort("timestamp", -1)
            .limit(3)
        )
        return render_template(
            "router_detail.html",
            router_ip=router_ip,
            records=records,
            error=None,
        )
    except PyMongoError:
        return (
            render_template(
                "router_detail.html",
                router_ip=router_ip,
                records=[],
                error="Cannot retrieve interface status from MongoDB.",
            ),
            503,
        )


@app.route("/add", methods=["POST"])
def add_router():
    ip = request.form.get("ip", "").strip()
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    if not ip or not username or not password:
        return redirect(url_for("index"))

    try:
        router_collection.insert_one(
            {"ip": ip, "username": username, "password": password}
        )
    except PyMongoError:
        return "Cannot save router information to MongoDB.", 503

    return redirect(url_for("index"))


@app.route("/delete/<router_id>", methods=["POST"])
def delete_router(router_id):
    try:
        router_collection.delete_one({"_id": ObjectId(router_id)})
    except (InvalidId, PyMongoError):
        pass

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, threaded=False)
