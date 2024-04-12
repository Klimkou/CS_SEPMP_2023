from flask import Flask
from flask import request
from flask import render_template
from flaskext.mysql import MySQL
from flask import jsonify, session
from flask_login import current_user, login_user, LoginManager, logout_user, login_required
from werkzeug.utils import redirect

mysql = MySQL()
login_manager = LoginManager()
app = Flask(__name__)
app.secret_key = "sasasdf2fb3443b4"
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'wf_tutorials'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
login_manager.init_app(app)


class User:
    name = ""
    password = ""
    id = 0

    def __init__(self, name="", password=""):
        self.name = name
        self.password = password

    def is_authenticated(self):
        query = "SELECT * from yii_users WHERE username=%s AND password=%s LIMIT 1"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(query, (self.name, self.password))
        data = cursor.fetchone()
        if data is None:
            return False
        else:
            self.id = data[0]
            return True

    def is_active(self):
        return True

    def is_anonymous(self):
        if self.id == 0:
            return True
        else:
            return False

    def get_id(self):
        return str(self.id).encode("utf-8").decode("utf-8")

    @staticmethod
    def get(user_id):
        query = "SELECT * from yii_users WHERE id =%s LIMIT 1"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(query, (user_id,))
        data = cursor.fetchone()
        user = User()
        user.id = user_id
        user.name = data[1]
        user.password = data[2]
        return user


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route("/")
def greeting():
    return "<h1 style='color:green'>Hello World!</h1>"


@app.route("/help")
def help():
    return "help me"


@app.route("/post/<id>")
def show_post(id):
    return "post id is " + id


@app.route("/bookmarks")
def display_bookmarks():
    bk = request.args.get("page", "1")
    return "the bookmark page is " + bk


@app.route("/index")
def index():
    users = ['user 1', 'user 2', 'users 3']
    data = {'pagetitle': 'wfTutorials', 'header': "Welcome to wftutorials", 'users': users, 'isloggedin': True}
    return render_template('index.html', data=data)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        name = request.form["username"]
        password = request.form["password"]
        user = User(name, password)
        if user.is_authenticated():
            login_user(user)
            return "logged in good"
        else:
            return "log in not good"
    else:
        return render_template('login.html')


@app.route('/countries')
def show_countries():
    query = "SELECT * from countries LIMIT 50"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    return render_template('countries.html', countries=data)


@app.route('/countries/create', methods=['POST', 'GET'])
def create_country():
    if request.method == "POST":
        newCountry = request.form["country"]
        query = "INSERT into countries(`country_name`) Values (%s)"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(query, (newCountry,))
        conn.commit()
        return "Country created: " + newCountry
    else:
        return render_template('create_country.html')


@app.route('/api/users', methods=['GET','POST'])
def api():
    if request.method == "GET":
        query = "SELECT * from countries LIMIT 50"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        return jsonify(data=data)
    if request.method == "POST":
        newCountry = request.form["country"]
        query = "INSERT into countries(`country_name`) Values (%s)"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(query, (newCountry,))
        conn.commit()
        return jsonify(results="Country created: " + newCountry)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')


if __name__ == "__main__":
    app.run(host='0.0.0.0')