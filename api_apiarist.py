from flask import Blueprint, request, jsonify, render_template, session

from database import *
from utils import role_required

apiarist_api = Blueprint('apiarist_api', __name__)


@apiarist_api.route("/", methods=['GET'])
@role_required('staff', 'admin')
def apiarist():
    # get all guides with primary image
    results = query("select * from user where role='apiarist';")
    print(results)
    return render_template('apiarist.html', user=session, apiarist_list=results)


@apiarist_api.route("/upload", methods=['GET'])
@role_required('admin')
def upload_guide_page():
    return render_template('register.html', user=session)


@apiarist_api.route("/<id>", methods=['GET'])
@role_required('admin')
def update_apiarist_page(id):
    result = query("select * from user where id=%s;", (id,))
    return render_template('edit_apiarist.html', user=result[0])


@apiarist_api.route("/<id>", methods=['PUT'])
@role_required('admin')
def update_apiarist(id):
    query("UPDATE user SET first_name=%s, last_name=%s, address=%s, email=%s, phone=%s, status=%s WHERE id=%s;",
          (request.json['first_name'], request.json['last_name'], request.json['address'], request.json['email'], request.json['phone'], request.json['status'], id))
    return jsonify({}), 200


@apiarist_api.route("/<id>", methods=['DELETE'])
@role_required('admin')
def delete_guide(id):
    print(id)
    query("DELETE FROM user WHERE id=%s;", (id,))
    return jsonify({}), 200
