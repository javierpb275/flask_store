from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import create_access_token

from db import db
from models import UserModel
from schemas import UserSchema

blp = Blueprint("Users", "users", description="Operations on users")


@blp.route("/api/users/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, body):
        user = UserModel(username=body["username"], password=pbkdf2_sha256.hash(body["password"]))
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return {"message": "User created successfully."}, 201


@blp.route("/api/users/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, body):
        user = UserModel.query.filter(UserModel.username == body["username"]).first()
        if user and pbkdf2_sha256.verify(body["password"], user.password):
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token}, 200
        abort(401, message="Invalid credentials.")


@blp.route("/api/users/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully."}, 200
