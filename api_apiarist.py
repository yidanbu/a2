from flask import Blueprint, request, jsonify, render_template, session

from database import *
from utils import role_required

# Blueprint for apiarist API
apiarist_api = Blueprint('apiarist_api', __name__)


# Webpage for apiarist list
@apiarist_api.route("/", methods=['GET'])
@role_required('staff', 'admin')
def apiarist():
    results = query("select * from user where role='apiarist';")
    return render_template('apiarist.html', user=session, apiarist_list=results)


# Webpage for admin register apiarist
@apiarist_api.route("/upload", methods=['GET'])
@role_required('admin')
def register_apiarist_page():
    return render_template('register.html', user=session)


# Webpage for admin edit apiarist profile
@apiarist_api.route("/<id>", methods=['GET'])
@role_required('admin')
def update_apiarist_page(id):
    result = query("select * from user where id=%s;", (id,))
    return render_template('edit_apiarist.html', user=session, apiarist=result[0])


# API for updating apiarist profile
@apiarist_api.route("/<id>", methods=['PUT'])
@role_required('admin')
def update_apiarist(id):
    query("UPDATE user SET first_name=%s, last_name=%s, address=%s, email=%s, phone=%s, status=%s WHERE id=%s;",
          (request.json['first_name'], request.json['last_name'], request.json['address'], request.json['email'], request.json['phone'], request.json['status'], id))
    return jsonify({}), 200


# API for delete apiarist
@apiarist_api.route("/<id>", methods=['DELETE'])
@role_required('admin')
def delete_apiarist(id):
    query("DELETE FROM user WHERE id=%s;", (id,))
    return jsonify({}), 200
