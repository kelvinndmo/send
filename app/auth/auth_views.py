from flask_restful import Resource
from flask import request
from werkzeug.security import check_password_hash
from utils import validators
from models.models import User
from flask_jwt_extended import create_access_token


class Signup(Resource):
    def post(self):
        '''add new user'''
        data = request.get_json()

        username = data['username']
        email = data['email']
        password = data['password']

        validate = validators.Validators()

        if not validate.valid_name(username):
            return {"message": "invalid username"}, 400

        if not validate.valid_email(email):
            return {"message": "invalid email adress"}, 400

        if not validate.valid_password(password):
            return {
                "message":
                    "Password should: contain a special character, \n \
                     and be at least 6 characters"}, 400

        if User().get_by_username(username):
            return {"message": "username already in use"}, 400
        if User().get_user_by_email(email):
            return {"message": "email adress already in use"}, 400

        user = User(username, email, password)
        user.add()

        return {
            "message": "account created successfully",
            "user": user.serialize()
        }, 201


class Login(Resource):
    def post(self):
        '''existing user can login'''

        data = request.get_json()

        username = data['username']
        password = data['password']

        user = User().get_by_username(username)
        print(user)

        if not user:
            return {"message": "user not found"}, 404
        if not check_password_hash(user.password, password):
            return {"message": "wrong password"}, 400

        token = create_access_token(user.username)

        return {
            "id": user.id,
            "token": token,
            "message": f"your were successfully logged in {username}"
        }, 200
