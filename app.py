import mysql.connector
from flask import Flask, session, redirect, url_for
from flask import render_template
from flask import request

import config

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')
app.secret_key = 'your_secret_key'
connection = None


def get_cursor():
    global connection
    connection = mysql.connector.connect(user=config.user,
                                         password=config.password,
                                         host=config.host,
                                         port=config.port,
                                         database=config.name,
                                         autocommit=True)
    return connection.cursor()


def query(stmt, params=None):
    cursor = get_cursor()
    cursor.execute(stmt, params)
    return cursor.fetchall()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']
        # hashed_password =users.get(email)
        # if hashed_password and check_password_hash(hashed_password, password):
        #     session['user_id'] = email  # 用户登录状态，存储在session中
        #     return redirect(url_for('index'))
        # else:
        #     return 'Login Failed'
        session['user_id'] = username
        return {"success": True}, 200
    return render_template('login.html')


@app.route('/')
@app.route("/index")
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)  # 移除用户登录状态
    return redirect(url_for('login'))


if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=8001, debug=False)
    app.run(host="0.0.0.0", port=8001, debug=True)
