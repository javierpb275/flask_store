import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores, items

blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/api/items/<string:item_id>")
class Item(MethodView):
    def get(self, item_id):
        try:
            return items[item_id], 200
        except KeyError:
            abort(404, message="Item Not Found")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted."}
        except KeyError:
            abort(404, message="Item Not Found")

    def put(self, item_id):
        body = request.get_json()
        if "price" not in body or "name" not in body:
            abort(400, message="Bad request. Ensure 'price' and 'name' are included in the JSON payload.")
        try:
            item = items[item_id]
            item |= body
            return item, 200
        except KeyError:
            abort(404, message="Item Not Found")


@blp.route("/api/items")
class ItemList(MethodView):
    def get(self):
        return {"items": list(items.values())}, 200

    def post(self):
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
