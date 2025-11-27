import db

def get_user(user_id): 
    sql = "SELECT id, username FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    print(f"Hakemassa käyttäjää ID: {user_id}, tulos: {result}")  # Debug-tulostus
    return result[0] if result else None

def get_register_dogs(user_id): 
    sql = """SELECT 
                rd.id AS dog_id, 
                rd.dogname, 
                rd.breed, 
                rd.age, 
                rd.gender 
             FROM 
                register_dog AS rd 
             WHERE 
                rd.user_id = ?"""
    result = db.query(sql, [user_id])
    return result