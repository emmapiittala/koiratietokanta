DROP TABLE IF EXISTS classes;
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

CREATE TABLE dog_classes (
    id INTEGER PRIMARY KEY,
    dog_id INTEGER REFERENCES register_dog(id),
    size TEXT,
    temperament TEXT,
    activity TEXT
);

CREATE TABLE questions (
    id INTEGER PRIMARY KEY,
    dog_id INTEGER REFERENCES register_dog(id),
    user_id INTEGER REFERENCES users(id),
    textarea TEXT
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    size TEXT NOT NULL,
    temperament TEXT NOT NULL,
    activity TEXT NOT NULL
);
DROP TABLE IF EXISTS sizes;
DROP TABLE IF EXISTS temperaments;
DROP TABLE IF EXISTS activities;

CREATE TABLE sizes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    size TEXT NOT NULL UNIQUE
);
CREATE TABLE temperaments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    temperament TEXT NOT NULL UNIQUE
);

CREATE TABLE activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    activity TEXT NOT NULL UNIQUE
);

INSERT INTO sizes (size) VALUES
('Pieni'),
('Keskikokoinen'),
('Suuri');

INSERT INTO temperaments (temperament) VALUES
('Kiltti'),
('Rauhallinen'),
('Leikkisä'),
('Hankaluutta vieraiden koirien seurassa'),
('Haukkuu herkästi'),
('Arka'),
('Aggressiivinen');

INSERT INTO activities (activity) VALUES
('Pentutreffit'),
('Näyttely'),
('Koirapuisto'),
('Ulkoiluun'),
('Agility'),
('Kisoihin'),
('Hoitoapua');

CREATE TABLE images (
    id INTEGER PRIMARY KEY,
    dog_id INTEGER REFERENCES register_dog(id),
    image BLOB
);