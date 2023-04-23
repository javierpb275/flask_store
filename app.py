import uuid
from flask import Flask, request
from db import items, stores
from flask_smorest import abort

app = Flask(__name__)


@app.get("/api/stores")
def get_stores():
    return {"stores": list(stores.values())}, 200


@app.get("/api/stores/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id], 200
    except KeyError:
        abort(404, message="Store Not Found")


@app.post("/api/stores")
def create_store():
    body = request.get_json()
    if "name" not in body:
        abort(
            400,
            message="Bad request. Ensure 'name' is included in the JSON payload.",
        )
    for store in stores.values():
        if body["name"] == store["name"]:
            abort(400, message=f"Store already exists.")
    store_id = uuid.uuid4().hex
    new_store = {**body, "id": store_id}
    stores[store_id] = new_store
    return new_store, 201


@app.get("/api/items")
def get_items():
    return {"items": list(items.values())}, 200


@app.get("/api/stores/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id], 200
    except KeyError:
        abort(404, message="Item Not Found")


@app.post("/api/items")
def create_item():
    body = request.get_json()
    if (
            "price" not in body
            or "store_id" not in body
            or "name" not in body
    ):
        abort(400, message="Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload.")
    for item in items.values():
        if (
                body["name"] == item["name"]
                and body["store_id"] == item["store_id"]
        ):
            abort(400, message=f"Item already exists.")
    if body["store_id"] not in stores:
        abort(404, message="Store Not Found")
    item_id = uuid.uuid4().hex
    new_item = {**body, "id": item_id}
    items[item_id] = new_item
    return new_item, 201


app.run()
