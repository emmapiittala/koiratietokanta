import db
import dogs
def add_dogs(dogname, breed, age, gender, user_id, classes):
    sql = """INSERT INTO register_dog (dogname, breed, age, gender, user_id)
              VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [dogname, breed, age, gender, user_id])
    dog_id = db.last_insert_id()

    size = None
    temperament = None
    activity = None

    for title, value in classes:
        if title == "size":
            size = value
        elif title == "temperament":
            temperament = value
        elif title == "activity":
            activity = value

    sql = "INSERT INTO dog_classes(dog_id, size, temperament, activity) VALUES (?, ?, ?, ?)"
    db.execute(sql, [dog_id, size, temperament, activity])  # Anna kaikki kolme arvoa

def add_question(dog_id, user_id, textarea):
        sql = """INSERT INTO questions (dog_id, user_id, textarea)
                  VALUES (?, ?, ?)"""
        db.execute(sql, [dog_id, user_id, textarea])

def get_question(dog_id):
    sql = """SELECT questions.textarea, questions.user_id, questions.dog_id, users.username
             FROM questions
             JOIN users ON questions.user_id = users.id
             WHERE questions.dog_id = ?
             ORDER BY questions.id DESC"""
    return db.query(sql, [dog_id])

def get_classes(dog_id):
    sql = "SELECT size, temperament, activity FROM dog_classes WHERE dog_id=?"
    return db.query(sql, [dog_id])

def get_dogs():
    sql = "SELECT id AS dog_id, dogname, user_id FROM register_dog ORDER BY id DESC"
    return db.query(sql)

def get_dog(dog_id):
    sql = """SELECT
        rd.id AS dog_id,
        rd.dogname,
        rd.breed,
        rd.age,
        rd.gender,
        dc.size,
        dc.temperament,
        dc.activity,
        u.id AS user_id,
        u.username AS user_name
    FROM register_dog AS rd
    JOIN users AS u ON rd.user_id = u.id
    LEFT JOIN dog_classes AS dc ON rd.id = dc.dog_id
    WHERE rd.id = ?"""

    result = db.query(sql, [dog_id])
    return result[0] if result else None


def update_dog(dog_id, dogname, breed, age, gender, size, temperament, activity):

    sql = """UPDATE register_dog SET dogname = ?, breed = ?, age = ?, gender = ? WHERE id = ?"""
    db.execute(sql, [dogname, breed, age, gender, dog_id])

    sql = "DELETE FROM dog_classes WHERE dog_id = ?"
    db.execute(sql, [dog_id])

    sql = "INSERT INTO dog_classes(dog_id, size, temperament, activity) VALUES (?, ?, ?, ?)"
    db.execute(sql, [dog_id, size, temperament, activity])

def remove_dog(dog_id):
    sql = "DELETE FROM questions WHERE dog_id = ?"
    db.execute(sql, [dog_id])

    sql = "DELETE FROM dog_classes WHERE dog_id = ?"
    db.execute(sql, [dog_id])

    sql = "DELETE FROM register_dog WHERE id = ?"
    db.execute(sql, [dog_id])


def find_dog(query):
    sql = """SELECT rd.id AS dog_id, rd.dogname, u.username, rd.user_id
             FROM register_dog AS rd
             JOIN users AS u ON rd.user_id = u.id
             WHERE rd.dogname LIKE ? OR rd.gender LIKE ? OR rd.breed LIKE ? OR rd.age LIKE ? OR u.username LIKE ?
             ORDER BY rd.id DESC"""
    query = "%" + query + "%"
    return db.query(sql, [query, query, query, query, query])

def get_dogs_for_user(user_id):
    sql = """SELECT id AS dog_id, dogname, breed, age, gender
    FROM register_dog WHERE user_id = ?"""
    return db.query(sql, [user_id])

def get_all_classes():
    sql = "SELECT size FROM sizes ORDER BY id"
    sizes = db.query(sql)

    sql = "SELECT temperament FROM temperaments ORDER BY id"
    temperaments = db.query(sql)

    sql = "SELECT activity FROM activities ORDER BY id"
    activities = db.query(sql)

    return {
        "sizes": [size[0] for size in sizes],
        "temperaments": [temperament[0] for temperament in temperaments],
        "activities": [activity[0] for activity in activities]
    }
def get_images(dog_id):
    sql = "SELECT id FROM images WHERE dog_id = ?"
    return db.query(sql, [dog_id])

def add_image(dog_id, image):
    sql = "INSERT INTO images (dog_id, image) VALUES (?, ?)"
    db.execute(sql, [dog_id, image])

def remove_image(dog_id, image_id):
    sql = "DELETE FROM images WHERE id = ? AND dog_id = ?"
    db.execute(sql, [image_id, dog_id])
def get_image(image_id):
    sql = "SELECT image FROM images WHERE id = ?"
    result = db.query(sql, [image_id])
    return result[0][0] if result else None