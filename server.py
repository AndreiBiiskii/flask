from typing import Type
import flask
from flask import Flask, jsonify, request
from flask.views import MethodView
from models import User, Session
from sqlalchemy.exc import IntegrityError
from schema import UpdateUser, CreatesUser
from pydantic import ValidationError

app = Flask('app')


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(response: flask.Response):
    request.session.close()
    return response


class HttpError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


@app.errorhandler(HttpError)
def error_event(error: HttpError):
    response = jsonify({"error": str(error.message)})
    response.status_code = error.status_code
    return response


def get_user_id(user_id: int):
    user = request.session.query(User).get(user_id)
    if user is None:
        raise HttpError(status_code=404, message="user no found")
    return user


def add_user(user: User):
    try:
        request.session.add(user)
        request.session.commit()
    except IntegrityError:
        raise HttpError(status_code=409, message="user already exists")


def validate_json(json_data: dict, schema_class: Type[CreatesUser] | Type[UpdateUser]):
    try:
        return schema_class(**json_data).dict(exclude_unset=True)
    except ValueError as er:
        error = er.errors()[0]
        error.pop("ctx", None)
        raise HttpError(status_code=400, message=error)


class UserView(MethodView):
    def get(self, user_id: int):
        user = get_user_id(user_id)
        return jsonify(user.dict)

    def post(self):
        user_data = validate_json(request.json, CreatesUser)
        user = User(**user_data)
        add_user(user)
        return jsonify(user.dict)

    def patch(self, user_id: int):
        user_data = validate_json(request.json, UpdateUser)
        user = get_user_id(user_id)
        for key, value in user_data.items():
            setattr(user, key, value)
        add_user(user)
        return jsonify(user.dict)

    def delete(self, user_id: int):
        user = get_user_id(user_id)
        request.session.delete(user)
        request.session.commit()
        return jsonify({"status": "user deleted"})


user_view = UserView.as_view('user_view')

app.add_url_rule('/user/<int:user_id>',
                 view_func=user_view,
                 methods=['GET', 'PATCH', 'DELETE'])

app.add_url_rule('/user/',
                 view_func=user_view,
                 methods=['POST', ])

if __name__ == '__main__':
    app.run()
