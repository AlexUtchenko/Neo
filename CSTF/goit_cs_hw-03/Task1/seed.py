import logging
from faker import Faker
import psycopg2
from psycopg2 import DatabaseError


# Підключення до бази даних
conn = psycopg2.connect(
    host="localhost", database="postgres", user="postgres", password="mysecretpassword"
)
cur = conn.cursor()

# налаштовуємо Faker під українську локалізацію призвища та імені
fake = Faker('uk_UA')

try:
    # Вставка даних для users
    cur = conn.cursor()
    for _ in range(5):
        fullname = fake.name()
        email = fake.email()
        cur.execute("INSERT INTO users (fullname, email) VALUES (%s, %s)", (fullname, email))
    conn.commit()

    # Вставка даних для tasks
    cur = conn.cursor()
    for _ in range(15):
        title = fake.sentence()
        description = fake.text()
        status_id = fake.random_int(min=1, max=3)  # Вибираємо випадковий статус
        user_id = fake.random_int(min=1, max=5)    # Вибираємо випадкового користувача
        cur.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
                    (title, description, status_id, user_id))
    conn.commit()

except DatabaseError as e:
    logging.error(e)
    conn.rollback()

finally:
    # Закриття підключення
    cur.close()
    conn.close()