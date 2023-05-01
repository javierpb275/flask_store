import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores, items
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/api/items/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item Not Found")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted."}
        except KeyError:
            abort(404, message="Item Not Found")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, body, item_id):
        try:
            item = items[item_id]
            item |= body
            return item
        except KeyError:
            abort(404, message="Item Not Found")


@blp.route("/api/items")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, body):
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
        return new_item
