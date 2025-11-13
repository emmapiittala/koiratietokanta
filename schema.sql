CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE register_dog (
    id INTEGER PRIMARY KEY,
    dogname TEXT,
    breed TEXT,
    age INTEGER,
    gender TEXT,
    user_id INTEGER REFERENCES users
);