import os

from flask import Flask, session, redirect, url_for, jsonify, render_template, request, Blueprint

from api_apiarist import apiarist_api
from api_dashboard import dashboard_api
from api_guide import guide_api
from api_profile import profile_api
from api_register import register_api
from api_staff import staff_api
from database import *
from utils import check_password

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')
app.secret_key = 'your_secret_key'
app.register_blueprint(register_api)
app.register_blueprint(guide_api, url_prefix='/guide')
app.register_blueprint(apiarist_api, url_prefix='/apiarist')
app.register_blueprint(staff_api, url_prefix='/staff')
app.register_blueprint(profile_api, url_prefix='/profile', static_url_path="/profile", static_folder="static")
app.register_blueprint(dashboard_api, url_prefix='/dashboard')
static_blueprint = Blueprint('static', __name__, static_url_path='/uploads', static_folder='uploads')
app.register_blueprint(static_blueprint)

# ensure upload folder exists
os.makedirs(config.upload_folder, exist_ok=True)
import werkzeug

@app.route("/me")
def me():
    print(dict(session))
    print(session)
    print(type(session))
    print(werkzeug.__version__)
    if 'username' not in session:
        return jsonify({"username": None}), 401
    return jsonify(dict(session)), 200


@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    print(username)
    result = query("select * from user where username=%s;", (username,))
    if not result:
        return {"success": False}, 403
    # compare password
    print(result[0]['password'], password)
    if not check_password(result[0]['password'], password):
        return {"success": False}, 403
    session['username'] = username
    session['role'] = result[0]['role']
    return {"success": True}, 200


@app.route('/')
@app.route("/index")
def index():
    return render_template('index.html', user=session)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=8001, debug=False)
    app.run(host="0.0.0.0", port=8001, debug=True)
