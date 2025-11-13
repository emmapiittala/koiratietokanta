import db

def add_dogs(dogname, breed, age, gender, user_id):

    sql = """INSERT INTO register_dog (dogname, breed, age, gender, user_id)
            VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [dogname, breed, age, gender, user_id])