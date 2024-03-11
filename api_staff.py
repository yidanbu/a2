import datetime

from flask import Blueprint, request, jsonify, render_template, session

from database import *
from utils import hash_password, role_required

staff_api = Blueprint('staff_api', __name__)


@staff_api.route("/", methods=['GET'])
@role_required('admin')
def staff():
    # get all guides with primary image
    results = query("select * from user where role='staff' or role='admin';")
    return render_template('staff.html', user=session, staff_list=results)


@staff_api.route("/upload", methods=['GET'])
@role_required('admin')
def upload_staff_page():
    return render_template('register_staff.html', user=session)


@staff_api.route("/upload", methods=['POST'])
@role_required('admin')
def register():
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


@staff_api.route("/<id>", methods=['GET'])
@role_required('admin')
def staff_detail_page(id):
    result = query("select * from user where id=%s;", (id,))
    return render_template('edit_staff.html', user=result[0])


@staff_api.route("/<id>", methods=['PUT'])
@role_required('admin')
def update_guide_basic_info(id):
    query("UPDATE user SET first_name=%s, last_name=%s, email=%s, phone=%s, position=%s, department=%s, status=%s, role=%s WHERE id=%s;",
          (request.json['first_name'], request.json['last_name'], request.json['email'], request.json['phone'], request.json['position'], request.json['department'], request.json['status'], request.json['role'], id))
    return jsonify({}), 200


@staff_api.route("/<id>", methods=['DELETE'])
@role_required('admin')
def delete_guide(id):
    query("DELETE FROM user WHERE id=%s;", (id,))
    return jsonify({}), 200
