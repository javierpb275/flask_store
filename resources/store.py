import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores

blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/api/stores/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        try:
            return stores[store_id], 200
        except KeyError:
            abort(404, message="Store Not Found")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted."}
        except KeyError:
            abort(404, message="Store Not Found")

    def put(self, store_id):
        body = request.get_json()
        if "name" not in body:
            abort(400, message="Bad request. Ensure 'name' is included in the JSON payload.")
        try:
            store = stores[store_id]
            store |= body
            return store, 200
        except KeyError:
            abort(404, message="Store Not Found")


@blp.route("/api/stores")
class StoreList(MethodView):
    def get(self):
        return {"stores": list(stores.values())}, 200

    def post(self):
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
