import os

from flask import Flask, session, redirect, url_for, jsonify, render_template, request, Blueprint

from api_guide import guide_api
from api_profile import profile_api
from api_register import register_api
from database import *
from utils import check_password

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')
app.secret_key = 'your_secret_key'
app.register_blueprint(register_api)
app.register_blueprint(guide_api, url_prefix='/guide')
app.register_blueprint(profile_api, url_prefix='/profile', static_url_path="/profile", static_folder="static")
static_blueprint = Blueprint('static', __name__, static_url_path='/uploads', static_folder='uploads')
app.register_blueprint(static_blueprint)

# ensure upload folder exists
os.makedirs(config.upload_folder, exist_ok=True)


@app.route("/me")
def me():
    if 'username' not in session:
        return jsonify({"username": None}), 401
    return jsonify({"username": session["username"]}), 200


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']
        print(username)
        result = query("select * from user where username=%s;", (username, ))
        if not result:
            return {"success": False}, 403
        # compare password
        print(result[0]['password'], password)
        if not check_password(result[0]['password'], password):
            return {"success": False}, 403
        session['username'] = username
        session['role'] = result[0]['role']
        return {"success": True}, 200
    return render_template('login.html')


@app.route('/')
@app.route("/index")
def index():
    # if 'user_id' not in session:
    #     return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/logout')
def logout():
    session.pop('username', None)  # 移除用户登录状态
    return redirect(url_for('login'))


if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=8001, debug=False)
    app.run(host="0.0.0.0", port=8001, debug=True)
