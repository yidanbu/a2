from flask import Blueprint, render_template, session, jsonify

from database import query
from utils import role_required

dashboard_api = Blueprint('dashboard_api', __name__)


@dashboard_api.route("/", methods=['GET'])
@role_required('apiarist', 'staff', 'admin')
def dashboard_page():
    if session['role'] == 'apiarist':
        return dashboard_apiarist()
    elif session['role'] == 'staff':
        return dashboard_staff()
    else:
        return dashboard_admin()


def dashboard_apiarist():
    type_ = query("select type, count(*) from guide GROUP BY type;")
    exists_in_nz = query("select exists_in_nz, count(*) from guide GROUP BY exists_in_nz;")
    if not type_ or not exists_in_nz:
        return jsonify({"result": "query failed"}), 500
    type_ = {item['type']: item['count(*)'] for item in type_}
    exists_in_nz = {item['exists_in_nz']: item['count(*)'] for item in exists_in_nz}
    return render_template('dashboard_apiarist.html', user=session, type=type_, exists_in_nz=exists_in_nz)


def dashboard_staff():
    type_ = query("select type, count(*) from guide GROUP BY type;")
    exists_in_nz = query("select exists_in_nz, count(*) from guide GROUP BY exists_in_nz;")
    user = query("select role, count(*) from user group by role;")
    if not type_ or not exists_in_nz or not user:
        return jsonify({"result": "query failed"}), 500
    type_ = {item['type']: item['count(*)'] for item in type_}
    exists_in_nz = {item['exists_in_nz']: item['count(*)'] for item in exists_in_nz}
    user = {item['role']: item['count(*)'] for item in user}
    apiarists_count = user['apiarist']
    return render_template('dashboard_staff.html', user=session, type=type_, exists_in_nz=exists_in_nz, apiarists_count=apiarists_count)


def dashboard_admin():
    type_ = query("select type, count(*) from guide GROUP BY type;")
    exists_in_nz = query("select exists_in_nz, count(*) from guide GROUP BY exists_in_nz;")
    user = query("select role, count(*) from user group by role;")
    if not type_ or not exists_in_nz or not user:
        return jsonify({"result": "query failed"}), 500
    type_ = {item['type']: item['count(*)'] for item in type_}
    exists_in_nz = {item['exists_in_nz']: item['count(*)'] for item in exists_in_nz}
    user = {item['role']: item['count(*)'] for item in user}
    apiarists_count = user['apiarist']
    staff_count = user['staff']
    admin_count = user['admin']
    return render_template('dashboard_admin.html', user=session, type=type_, exists_in_nz=exists_in_nz,
                           apiarists_count=apiarists_count, staff_count=staff_count, admin_count=admin_count)
