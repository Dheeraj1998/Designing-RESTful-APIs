from flask import Flask, request, g
from flask_httpauth import HTTPBasicAuth
from model_2 import Base, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import hashlib
import json

engine = create_engine('sqlite:///users.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

auth = HTTPBasicAuth()
app = Flask(__name__)


@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    else:
        temp_username = None
        temp_password = None

        for value in session.query(User).filter_by(username=username):
            temp_username = value.username
            temp_password = value.password

        if temp_password is None:
            return False

        else:
            check_user = User(username=temp_username, password=temp_password)

            if check_user.verify_password(password=password):
                g.User = session.query(User).filter_by(username=username).first()
                return True
            else:
                return False


@app.route('/createUser', methods=['GET'])
def create_user():
    username = request.args.get('username')
    password = request.args.get('password')

    new_user = User(username=username, password=password)
    new_user.hash_password()
    session.add(new_user)
    session.commit()

    return new_user.print_details()


@app.route('/modifyUser', methods=['GET'])
@auth.login_required
def modify_user():
    new_password = request.args.get("password")

    user_data = session.query(User).filter_by(username=request.authorization["username"]).first()
    user_data.password = str(hashlib.sha3_256(new_password.encode()).hexdigest())
    session.commit()

    return json.dumps({"message": "Password has been successfully changed!"})


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


@app.route('/generateToken')
@auth.login_required
def generate_token():
    token_value = g.User.generate_token()

    final_result = {"token": str(token_value)[2:-1]}
    return json.dumps(final_result)


@app.route('/verifyToken', methods=['GET'])
def verify_token():
    token_value = request.args.get("token_value")
    final_value = User.verify_token(token_value)

    if final_value is None:
        return json.dumps({"error": "Not a valid token value."})

    return json.dumps(final_value)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
