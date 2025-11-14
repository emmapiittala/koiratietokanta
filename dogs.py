import db

def add_dogs(dogname, breed, age, gender, user_id): ##Lisää uuden koiran tietokantaan

    sql = """INSERT INTO register_dog (dogname, breed, age, gender, user_id)
            VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [dogname, breed, age, gender, user_id])

def get_dogs(): ## tämä hakee kaikki koirat register_dog
    sql = "SELECT id, dogname FROM register_dog ORDER BY id DESC"
    return db.query(sql)

def get_dog(dog_id): ##Hakee tietyn koiran tiedot
    sql = """SELECT
    rd.id AS dog_id,
    rd.dogname,
    rd.breed,
    rd.age,
    rd.gender,
    u.id AS user_id,
    u.username AS user_name
    FROM register_dog AS rd
    JOIN users AS u ON rd.user_id = u.id
    WHERE rd.id = ?"""

    result = db.query(sql, [dog_id])

    return result[0] if result else None

def update_dog(dog_id,dogname, breed, age, gender): ##voi päivittää koiran tietoja/ilmoitusta.
    sql = """UPDATE register_dog SET dogname = ?,
    breed = ?,
    age = ?,
    gender = ?
    WHERE id = ?"""
    db.execute(sql, [dogname, breed, age, gender, dog_id])

def remove_dog(dog_id): ##Poistaa koiran
    sql = "DELETE FROM register_dog WHERE id = ?"
    db.execute(sql, [dog_id])