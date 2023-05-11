from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import ItemModel

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
        item = ItemModel(**body)
        try:
            db.session.add(item)
            db.session.commit()
        except IntegrityError:
            abort(400, message='An item with that name already exists')
        except SQLAlchemyError:
            abort(500, message='An error occurred while inserting the item')

        return item
