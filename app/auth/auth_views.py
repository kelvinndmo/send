from flask import Flask


from flask_restful import Resource, reqparse

from models.models import User, Users

from utils import validators

from werkzeug.security import check_password_hash

from flask_jwt_extended import create_access_token

import datetime


class SignUp(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument("username", type=str, required=True,
                        help="This field can not be left bank")
    parser.add_argument("email", type=str, required=True,
                        help="This field can not be left bank")
    parser.add_argument("password", type=str, required=True,
                        help="This field can not be left bank")
    parser.add_argument("is_admin", type=int, required=True,
                        help="This field can not be left bank")

    def post(self):
        """ Create a new user"""
        data = SignUp.parser.parse_args()

        username = data["username"]
        email = data["email"]
        password = data["password"]
        is_admin = data["is_admin"]

        validate = validators.Validators()

        if not validate.valid_name(username):
            return {"message": "username must contain alphanumeric"
                    " characters only"}, 400

        if not validate.valid_email(email):
            return {"message": "enter valid email"}, 400

        if not validate.valid_password(password):
            return {"message": "password should start with a capital letter"
                    " and include a number"}, 400

        if is_admin not in range(0, 2):
            return {"message": " must be one or zero"}, 400

        if User().get_by_username(username):
            return {"message": f"user {username} already exists"}, 400

        if User().get_by_email(email):
            return {"message": f"user with {email} already exists"}, 400

        user = User(username, email, password, bool(is_admin))

        Users.append(user)

        return {"message": f"user {username} created successfully"}, 201


class Login(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument("username", type=str, required=True,
                        help="This field can not be left bank")
    parser.add_argument("password", type=str, required=True,
                        help="This field can not be left bank")

    def post(self):
        data = Login.parser.parse_args()

        username = data["username"]
        password = data["password"]

        validate = validators.Validators()

        if not validate.valid_name(username):
            return {"message": "username must contain alphanumeric"
                    " characters only"}, 400

        if not validate.valid_name(password):
            return {"message": "password should start with a capital letter"
                    " and include a number"}, 400

        user = User().get_by_username(username)

        if user and check_password_hash(user.password_hash, password):
            expires = datetime.timedelta(minutes=30)
            token = create_access_token(User.user_id, expires_delta=expires)
            return {'token': token, 'message': 'successfully logged'}, 200
        return {'message': 'user not found'}, 404
