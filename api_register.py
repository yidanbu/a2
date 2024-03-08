import datetime

from flask import Blueprint, request, jsonify, render_template, session

from database import *
from utils import hash_password

register_api = Blueprint('register_api', __name__)


@register_api.route("/register", methods=['POST'])
def register():
    query(
        "insert into user (username, password, role, first_name, last_name, address, email, phone, date_hired_or_joined, status) "
        "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ;",
        (
            request.json['username'],
            hash_password(request.json['password']),
            'apiarist',
            request.json['first_name'],
            request.json['last_name'],
            request.json['address'],
            request.json['email'],
            request.json['phone'],
            datetime.datetime.now(),
            'active',
        ))
    return jsonify({}), 200


@register_api.route("/register", methods=['GET'])
def register_page():
    return render_template('register.html', user=session)


@register_api.route("/username/check", methods=['POST'])
def check_username_exists():
    username = request.json['username']
    # query database to check username exists
    result = query("SELECT * FROM user WHERE username = %s", (username,))
    print(result)
    if result:
        return jsonify({"exists": "yes"}), 409
    return jsonify({"exists": "no"}), 200
