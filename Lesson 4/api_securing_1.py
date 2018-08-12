from flask import Flask, request
from model_1 import Base, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import json

engine = create_engine('sqlite:///users.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)


@app.route('/createUser', methods=['GET'])
def create_user():
    username = request.args.get('username')
    password = request.args.get('password')

    new_user = User(username=username, password=password)
    new_user.hash_password()
    session.add(new_user)
    session.commit()

    return new_user.print_details()


@app.route('/verifyUser', methods=['GET'])
def verify_user():
    username = request.args.get('username')
    password = request.args.get('password')

    temp_username = None
    temp_password = None

    for value in session.query(User).filter_by(username=username):
        temp_username = value.username
        temp_password = value.password

    if temp_password is None:
        error_message = {"error": "No user found."}
        return json.dumps(error_message)

    else:
        check_user = User(username=temp_username, password=temp_password)

        if check_user.verify_password(password=password):
            user_value = {temp_username: temp_password}
            return json.dumps(user_value)
        else:
            error_message = {"error": "Not a valid password."}
            return json.dumps(error_message)


@app.route('/showUsers')
def show_users():
    all_data = session.query(User).all()
    final_result = {}

    for value in all_data:
        final_result[value.username] = value.password

    final_result = json.dumps(final_result)
    return final_result


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
