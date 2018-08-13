from datetime import timedelta
from flask import Flask, request
from model_3 import Base, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import datetime
import json

engine = create_engine('sqlite:///rate_limiting.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)


@app.route('/createUser', methods=['GET'])
def create_user():
    username = request.args.get('username')

    new_user = User(username=username)
    session.add(new_user)
    session.commit()

    return new_user.print_details()


@app.route('/showUsers')
def show_users():
    all_data = session.query(User).all()
    final_result = {}

    for value in all_data:
        final_result[value.username] = [value.rate_limit, value.register_date]

    final_result = json.dumps(final_result, default=str)
    return final_result


@app.route('/useAPI', methods=['GET'])
def use_api():
    username = request.args.get("username")
    user_data = session.query(User).filter_by(username=username).first()
    days_difference = datetime.datetime.now() - user_data.register_date
    final_result = {}

    if days_difference.days == 0 and user_data.rate_limit < 100:
        user_data.rate_limit += 1
        session.commit()

        user_data = session.query(User).filter_by(username=username).first()
        final_result[user_data.username] = [user_data.rate_limit, user_data.register_date]
        return json.dumps(final_result, default=str)

    elif days_difference.days == 0:
        final_result["error_message"] = "The daily rate has been exhausted!"
        return json.dumps(final_result)

    else:
        user_data.rate_limit = 0
        user_data.register_date = datetime.datetime.now() + timedelta(days=days_difference.days)

        user_data = session.query(User).filter_by(username=username).first()
        final_result[user_data.username] = [user_data.rate_limit, user_data.register_date]
        return json.dumps(final_result, default=str)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
