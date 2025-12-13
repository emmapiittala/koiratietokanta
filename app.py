import secrets
from flask import Flask, abort, flash, make_response
import sqlite3
from flask import Flask
from flask import url_for
from flask import redirect, render_template, request, session
import markupsafe
import db
import dogs
import users
import config

app = Flask(__name__)
app.secret_key = config.secret_key


@app.route("/")
def index():
    all_dogs = dogs.get_dogs()
    dogs_with_usernames = []

    if not all_dogs:
        return render_template("index.html", dogs=[])

    for dog in all_dogs:
        user = users.get_user(dog['user_id'])
        question_count = dogs.get_question_count(dog['dog_id'])
        dog_info = {
            'id': dog['dog_id'],
            'dogname': dog['dogname'],
            'user_id': dog['user_id'],
            'user_name': user['username'] if user else "Tuntematon",
            'question_count': question_count
        }
        dogs_with_usernames.append(dog_info)

    return render_template("index.html", dogs=dogs_with_usernames)

@app.route("/find_dog")
def find_dog():
    query = request.args.get("query")
    queston_text = ""
    if query:
        results = dogs.find_dog(query)
    else:
        results = []
    return render_template("find_dog.html", query=query, result=results, queston_text = queston_text)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if user is None:
        abort(404)
    user_dogs = dogs.get_dogs_for_user(user_id)
    classes = dogs.get_classes(user_id)
    questions = []
    if user_dogs:
        for dog in user_dogs:
            dog_questions = dogs.get_question(dog['dog_id'])
            questions.extend(dog_questions)
    return render_template("show_user.html", user=user, dogs=user_dogs, classes=classes,questions=questions)

@app.route("/dogs/<int:dog_id>")
def get_dog(dog_id):
    session["csrf_token"] = secrets.token_hex(16)
    dog = dogs.get_dog(dog_id)
    if dog is None:
        abort(404)
    classes = dogs.get_classes(dog_id)
    questions = dogs.get_question(dog_id)
    images = dogs.get_images(dog_id)
    question_text = ""
    return render_template("show_dog.html", dog=dog, classes = classes, questions = questions, question_text = question_text, images = images)

@app.route("/register_dog")
def register_dog():
    session["csrf_token"] = secrets.token_hex(16)
    all_classes = dogs.get_all_classes()
    return render_template("register_dog.html", 
        sizes=all_classes["sizes"], 
        temperaments=all_classes["temperaments"], 
        activities=all_classes["activities"])

@app.route("/dogs/")
def list_dogs():
    all_dogs = dogs.get_dogs()
    return render_template("list_dogs.html", dogs=all_dogs)

@app.route("/create_questions", methods=["POST"])
def create_questions():
    check_csrf()
    if "user_id" not in session:
        abort(403)
    dog_id = request.form["dog_id"]
    user_id = session["user_id"]
    textarea = request.form["textarea"]

    dogs.add_question(dog_id, user_id, textarea)
    flash("Kysymys lähetetty")
    return redirect("/dogs/" + str(dog_id))

@app.route("/create_register_dog", methods=["POST"])
def create_register_dog():
    check_csrf()
    if "user_id" not in session:
        abort(403)

    user_id = session["user_id"]
    dogname = request.form["dogname"]
    breed = request.form["breed"]
    age = request.form["age"]
    gender = request.form["gender"]
    size = request.form.get("size")
    temperament = request.form.get("temperament")
    activity = request.form.get("activity")

    classes = []
    if size:
        classes.append(("size", size))
    if temperament:
        classes.append(("temperament", temperament))
    if activity:
        classes.append(("activity", activity))

        if not dogname or len(dogname) >= 50:
            flash("VIRHE: Nimi ei voi olla yli 50 merkkiä pitkä")
            return redirect("/dogs/" + str(dog_id))
        if len(breed) >= 50:
            flash("VIRHE: Rotu ei voi olla yli 50 merkkiä pitkä")
            return redirect("/dogs/" + str(dog_id))
        if int(age) < 0:
            flash("VIRHE: Ikä ei voi olla negatiivinen.")
            return redirect("/dogs/" + str(dog_id))
        if int(age) >= 35:
            flash("VIRHE: Tarkista ikä")
            return redirect("/dogs/" + str(dog_id))

    all_classes = dogs.get_all_classes()

    for entry in classes:
        title, value = entry
        if title == "size" and value not in all_classes["sizes"]:
            print(f"Virheellinen luokka: {title}, arvo: {value}")
            abort(403)
        elif title == "temperament" and value not in all_classes["temperaments"]:
            print(f"Virheellinen luokka: {title}, arvo: {value}")
            abort(403)
        elif title == "activity" and value not in all_classes["activities"]:
            print(f"Virheellinen luokka: {title}, arvo: {value}")
            abort(403)

    dogs.add_dogs(dogname, breed, age, gender, user_id, classes)

    dog_id = db.last_insert_id()
    flash("Koira rekisteröity onnistuneesti.")
    return redirect("/dogs/" + str(dog_id))

@app.route('/edit_dog/<int:dog_id>', methods=['GET', 'POST'])
def edit_dog(dog_id):
    dog = dogs.get_dog(dog_id)
    if dog is None:
        abort(404)

    if "user_id" not in session or dog["user_id"] != session["user_id"]:
        abort(403)
    if request.method == 'GET':
        session["csrf_token"] = secrets.token_hex(16)

    all_classes = dogs.get_all_classes()

    if request.method == 'POST':
        check_csrf()
        dogname = request.form["dogname"]
        breed = request.form["breed"]
        age = request.form["age"]
        gender = request.form["gender"]
        size = request.form.get("size")
        temperament = request.form.get("temperament")
        activity = request.form.get("activity")

        if not dogname or len(dogname) >= 50:
            flash("VIRHE: Nimi ei voi olla yli 50 merkkiä pitkä")
            return redirect("/dogs/" + str(dog_id))
        if len(breed) >= 50:
            flash("VIRHE: Rotu ei voi olla yli 50 merkkiä pitkä")
            return redirect("/dogs/" + str(dog_id))
        if int(age) < 0:
            flash("VIRHE: Ikä ei voi olla negatiivinen.")
            return redirect("/dogs/" + str(dog_id))
        if int(age) >= 35:
            flash("VIRHE: Tarkista ikä")
            return redirect("/dogs/" + str(dog_id))

        validate_classes(all_classes, size, temperament, activity)
        dogs.update_dog(dog_id, dogname, breed, age, gender, size, temperament, activity)
        flash("Koiran tiedot päivitetty")
        return redirect(url_for('get_dog', dog_id=dog_id))

    return render_template('edit_dog.html', dog=dog,
                           sizes=all_classes["sizes"],
                           temperaments=all_classes["temperaments"],
                           activities=all_classes["activities"])

def validate_classes(all_classes, size, temperament, activity):
    classes = [("size", size), ("temperament", temperament), ("activity", activity)]
    for title, value in classes:
        if value and title == "size" and value not in all_classes["sizes"]:
            abort(403)
        elif value and title == "temperament" and value not in all_classes["temperaments"]:
            abort(403)
        elif value and title == "activity" and value not in all_classes["activities"]:
            abort(403)

@app.route("/images/<int:dog_id>")
def edit_images(dog_id):
    require_login()
    dog = dogs.get_dog(dog_id)
    if dog is None:
        abort(404)
    if "user_id" not in session or dog["user_id"] != session["user_id"]:
        abort(403)

    images = dogs.get_images(dog_id)
    return render_template("images.html", dog=dog, images=images)

@app.route("/add_image", methods=["POST"])
def add_image():
    require_login()
    check_csrf()

    dog_id = request.form["dog_id"]
    file = request.files["image"]
    dog = dogs.get_dog(dog_id)

    if dog is None:
        abort(404)

    if "user_id" not in session or dog["user_id"] != session["user_id"]:
        abort(403)

    if not file or not file.filename.endswith((".png")):
        flash("VIRHE: Lähettämäsi tiedosto ei ole .png-tiedosto")
        return redirect("/add_image")

    image = file.read()
    if len(image) > 100 * 1024:
        flash("VIRHE: Lähettämäsi tiedosto on liian suuri")
        return redirect("/add_image")

    dogs.add_image(dog_id, image)
    flash("Kuva tallennettu")
    return redirect("/dogs/" + str(dog_id))


@app.route("/remove_images", methods=["POST"])
def remove_images():
    require_login()
    check_csrf()

    dog_id = request.form["dog_id"]
    dog = dogs.get_dog(dog_id)
    if dog is None:
        abort(404)

    if "user_id" not in session or dog["user_id"] != session["user_id"]:
        abort(403)

    for image_id in request.form.getlist("image_id"):
        dogs.remove_image(dog_id, image_id)
    flash("Kuvia poistettu")
    return redirect("/images/" + str(dog_id))

@app.route("/image/<int:image_id>")
def show_image(image_id):
    image = dogs.get_image(image_id)
    if not image:
        abort(404)

    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/png")
    return response

@app.route("/remove_dog/<int:dog_id>", methods=["GET", "POST"])
def remove_dog(dog_id):
    dog = dogs.get_dog(dog_id)
    if dog is None:
        abort(404)
    if dog["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        session["csrf_token"] = secrets.token_hex(16)
    if request.method == "POST":
        check_csrf()
        dogs.remove_dog(dog_id)
        return redirect(url_for('index'))
    else:
        dog = dogs.get_dog(dog_id)
        return render_template("remove_dog.html", dog = dog)

@app.route("/register")
def register():
    session["csrf_token"] = secrets.token_hex(16)
    return render_template("register.html")


@app.route("/create", methods=["POST"])
def create():
    check_csrf()
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if password1 != password2:
        flash("VIRHE: salasanat eivät ole samat")
        return render_template("register.html")
    try:
        users.create_user(username, password1)
        flash("Tunnus luotu onnistuneesti.")
        return render_template("register.html")
    except sqlite3.IntegrityError:
        flash("VIRHE: tunnus on jo varattu")
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        session["csrf_token"] = secrets.token_hex(16)
        return render_template("login.html")

    if request.method == "POST":
        check_csrf()
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            flash("VIRHE: Väärä tunnus tai salasana")
            return render_template("login.html")

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
    if "username" in session:
        del session["username"]
    return redirect("/")

def check_csrf():
    if "csrf_token" not in session:
        abort(403)

    token_from_form = request.form.get("csrf_token")
    token_from_session = session["csrf_token"]

    if not token_from_form or token_from_form != token_from_session:
        abort(403)

@app.route("/new_message", methods=["POST"])
def new_message():
    check_csrf()

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)