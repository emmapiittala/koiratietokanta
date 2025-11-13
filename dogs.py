import db

def add_dogs(dogname, breed, age, gender, user_id):

    sql = """INSERT INTO register_dog (dogname, breed, age, gender, user_id)
            VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [dogname, breed, age, gender, user_id])

def get_dogs():
    sql = "SELECT id, dogname FROM register_dog ORDER BY id DESC"
    return db.query(sql)

def get_dog(dog_id):
    sql = """SELECT
    rd.id AS dog_id,
    rd.dogname,
    rd.breed,
    rd.age,
    rd.gender,
    u.username AS user_name
    FROM register_dog AS rd
    JOIN users AS u ON rd.user_id = u.id
    WHERE rd.id = ?"""

    result = db.query(sql, [dog_id])

    return result[0] if result else None