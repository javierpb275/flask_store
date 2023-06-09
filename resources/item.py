from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required, get_jwt

from db import db
from models import ItemModel

from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/api/items/<int:item_id>")
class Item(MethodView):

    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    @jwt_required()
    def delete(self, item_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required")
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted"}, 200

    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, body, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.price = body["price"]
            item.name = body["name"]
        else:
            item = ItemModel(id=item_id, **body)
        db.session.add(item)
        db.session.commit()
        return item


@blp.route("/api/items")
class ItemList(MethodView):

    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @jwt_required(fresh=True)
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
