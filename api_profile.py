from flask import Blueprint, request, jsonify, render_template, session

from database import *
from utils import hash_password

profile_api = Blueprint('profile_api', __name__)


@profile_api.route("/", methods=['GET'])
def profile_page():
    if 'username' not in session:
        return jsonify({"username": None}), 401
    result = query("select * from user where username=%s;", (session['username'],))
    if not result:
        return jsonify({"username": None}), 401
    return render_template('profile.html', user=result[0])


@profile_api.route("/<id>", methods=['PUT'])
def update_profile(id):
    # TODO check valid
    if request.json['password']:
        query("update user set password=%s, first_name=%s, last_name=%s, address=%s, email=%s, phone=%s where id=%s;",
              (hash_password(request.json['password']), request.json['first_name'], request.json['last_name'], request.json['address'], request.json['email'], request.json['phone'], id))
    else:
        query("update user set first_name=%s, last_name=%s, address=%s, email=%s, phone=%s where id=%s;",
              (request.json['first_name'], request.json['last_name'], request.json['address'], request.json['email'], request.json['phone'], id))
    return jsonify({"message": "Profile updated successfully."}), 200
