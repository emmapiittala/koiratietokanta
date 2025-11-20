from flask import Flask, abort
import sqlite3
from flask import Flask
from flask import url_for
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import db
import config
import dogs


app = Flask(__name__)
app.secret_key = config.secret_key


@app.route("/")
def index():
    all_dogs = dogs.get_dogs()
    return render_template("index.html", dogs=all_dogs)

@app.route("/find_dog")
def find_dog():
    query = request.args.get("query")
    if query:
        results = dogs.find_dog(query)
    else:
        query = ""
        results = []
    return render_template("find_dog.html", query =query, result=results)

@app.route("/dogs/<int:dog_id>")
def get_dog(dog_id):
    dog = dogs.get_dog(dog_id)
    return render_template("show_dog.html", dog=dog)


@app.route("/register_dog")
def register_dog():
    return render_template("register_dog.html")

@app.route("/create_register_dog", methods=["POST"])
def create_register_dog():
    dogname = request.form["dogname"]
    breed = request.form["breed"]
    age = request.form["age"]
    gender = request.form["gender"]
    user_id = session["user_id"]

    if int(age) < 0:
        return "VIRHE: Ikä ei voi olla negatiivinen."

    dogs.add_dogs(dogname, breed, age, gender, user_id)

    return redirect("/")

@app.route('/edit_dog/<int:dog_id>', methods=['GET', 'POST'])
def edit_dog(dog_id):
    dog = dogs.get_dog(dog_id)
    if dog["user_id"] != session["user_id"]:
        abort(403)

    if request.method == 'POST':
        dogname = request.form["dogname"]
        breed = request.form["breed"]
        age = request.form["age"]
        gender = request.form["gender"]

        dogs.update_dog(dog_id, dogname, breed, age, gender)
        return redirect(url_for('get_dog', dog_id=dog_id))
    else:
        dog = dogs.get_dog(dog_id)
        return render_template('edit_dog.html', dog=dog)

@app.route("/update_dog", methods=["POST"])
def update_dog():
    dog_id = request.form["dog_id"]
    dog = dogs.get_dog(dog_id)
    if dog["user_id"] != session["user_id"]:
        abort(403)

    dog_id = request.form["dog_id"]
    dogname = request.form["dogname"]
    breed = request.form["breed"]
    age = request.form["age"]
    gender = request.form["gender"]

    dogs.update_dog(dog_id, dogname, breed, age, gender)
    return redirect(url_for('get_dog', dog_id=dog_id))

@app.route("/remove_dog/<int:dog_id>", methods=["GET", "POST"])
def remove_dog(dog_id):
    dog = dogs.get_dog(dog_id)
    if dog["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "POST":
        dogs.remove_dog(dog_id)
        return redirect(url_for('index'))
    else:
        dog = dogs.get_dog(dog_id)
        return render_template("remove_dog.html", dog = dog)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if password1 != password2:
        return render_template("register.html", error="VIRHE: salasanat eivät ole samat")

    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return render_template("register.html", error="VIRHE: tunnus on jo varattu")

    return render_template("register.html", success="Tunnus luotu onnistuneesti")

@app.route("/login", methods=["GET","POST"])

def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])

    if result:
            user_id = result[0]["id"]
            password_hash = result[0]["password_hash"]

            if check_password_hash(password_hash, password):
                session["user_id"] = user_id
                session["username"] = username
                return redirect("/")
            else:
                return render_template("login.html", error="VIRHE: Väärä tunnus tai salasana")
    else:
        return render_template("login.html", error="VIRHE: käyttäjätunnusta ei löytynyt")

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
    if "username" in session:
        del session["username"]
    return redirect("/")
