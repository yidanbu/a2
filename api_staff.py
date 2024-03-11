import datetime

from flask import Blueprint, request, jsonify, render_template, session

import utils
from database import *
from utils import hash_password, role_required

# Blueprint for staff API
staff_api = Blueprint('staff_api', __name__)


# Webpage for staff list
@staff_api.route("/", methods=['GET'])
@role_required('admin')
def staff():
    results = query("select * from user where role='staff' or role='admin';")
    return render_template('staff.html', user=session, staff_list=results)


# Webpage for admin register staff
@staff_api.route("/upload", methods=['GET'])
@role_required('admin')
def upload_staff_page():
    return render_template('register_staff.html', user=session)


# API for register staff
@staff_api.route("/upload", methods=['POST'])
@role_required('admin')
def register():
    if not utils.check_password(request.json['password']) or not utils.check_email(request.json['email']):
        return jsonify({"message": "Invalid password format or email."}), 400
    query(
        "insert into user (username, password, role, first_name, last_name,  email, phone, date_hired_or_joined, status, position, department) "
        "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ;",
        (
            request.json['username'],
            hash_password(request.json['password']),
            request.json['role'],
            request.json['first_name'],
            request.json['last_name'],
            request.json['email'],
            request.json['phone'],
            datetime.datetime.now(),
            'active',
            request.json['position'],
            request.json['department']
        ))
    return jsonify({}), 200


# Webpage for admin edit staff profile
@staff_api.route("/<id>", methods=['GET'])
@role_required('admin')
def staff_detail_page(id):
    result = query("select * from user where id=%s;", (id,))
    return render_template('edit_staff.html', user=result[0])


# API for updating staff profile
@staff_api.route("/<id>", methods=['PUT'])
@role_required('admin')
def update_guide_basic_info(id):
    query("UPDATE user SET first_name=%s, last_name=%s, email=%s, phone=%s, position=%s, department=%s, status=%s, role=%s WHERE id=%s;",
          (request.json['first_name'], request.json['last_name'], request.json['email'], request.json['phone'], request.json['position'], request.json['department'], request.json['status'], request.json['role'], id))
    return jsonify({}), 200


# API for delete staff
@staff_api.route("/<id>", methods=['DELETE'])
@role_required('admin')
def delete_guide(id):
    query("DELETE FROM user WHERE id=%s;", (id,))
    return jsonify({}), 200
