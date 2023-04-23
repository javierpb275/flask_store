import uuid

from flask import Flask, request
from db import items, stores

app = Flask(__name__)


@app.get("/api/stores")
def get_stores():
    return {"stores": list(stores.values())}, 200


@app.get("/api/stores/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id], 200
    except KeyError:
        return {"message": "Store Not Found"}, 404


@app.post("/api/stores")
def create_store():
    body = request.get_json()
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
        return {"message": "Item Not Found"}, 404


@app.post("/api/items")
def create_item():
    body = request.get_json()
    if body["store_id"] not in stores:
        return {"message": "Store Not Found"}, 404

    item_id = uuid.uuid4().hex
    new_item = {**body, "id": item_id}
    items[item_id] = new_item
    return new_item, 201


app.run()
