import logging

import psycopg2
from psycopg2 import DatabaseError


# Підключення до бази даних
conn = psycopg2.connect(
    host="localhost", database="postgres", user="postgres", password="mysecretpassword"
)
cur = conn.cursor()

# sql команда для створення таблиць
sql = """
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    fullname VARCHAR(100),
    email VARCHAR(100) UNIQUE
);

CREATE TABLE status (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE,
    CONSTRAINT status_name_unique UNIQUE (name)
);

INSERT INTO status (name) VALUES 
('new'),
('in progress'),
('completed');

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100),
    description TEXT,
    status_id INTEGER REFERENCES status(id),
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);

"""

# виконуємо команди
cur.execute(sql)

try:
    # Збереження змін
    conn.commit()
except DatabaseError as e:
    logging.error(e)
    conn.rollback()
finally:
    # Закриття підключення
    cur.close()
    conn.close()
