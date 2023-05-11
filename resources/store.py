from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import StoreModel

from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/api/stores/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="Store Not Found")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted."}
        except KeyError:
            abort(404, message="Store Not Found")

    @blp.response(200, StoreSchema)
    def put(self, store_id):
        body = request.get_json()
        if "name" not in body:
            abort(400, message="Bad request. Ensure 'name' is included in the JSON payload.")
        try:
            store = stores[store_id]
            store |= body
            return store
        except KeyError:
            abort(404, message="Store Not Found")


@blp.route("/api/stores")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return stores.values()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, body):
        store = StoreModel(**body)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message='A store with that name already exists')
        except SQLAlchemyError:
            abort(500, message='An error occurred while creating the store')

        return store
