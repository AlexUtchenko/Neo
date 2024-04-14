import psycopg2
from psycopg2 import DatabaseError


# шаблон на запит до бази даних
def execute_query(query, *args):
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="mysecretpassword",
        )
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        return rows
    except psycopg2.Error as e:
        print("Error executing query:", e)
    finally:
        if conn:
            conn.close()


# шблон на зміни в базі
def to_change_query(query, *args):
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="mysecretpassword",
        )
        cur = conn.cursor()
        cur.execute(query, *args)
        conn.commit()
        print("Запит виконаний успішно.")
    except psycopg2.Error as e:
        print("Помилка виконання запиту:", e)
    finally:
        if conn:
            conn.close()


def task1(user_id):
    """
    Отримати всі завдання певного користувача. Використайте SELECT для отримання завдань конкретного користувача за його user_id.
    """
    query = f"SELECT id, title FROM tasks WHERE user_id = {user_id};"
    return execute_query(query)


def task2(status):
    """
    Вибрати завдання за певним статусом. Використайте підзапит для вибору завдань з конкретним статусом, наприклад, 'new'.
    """
    if status not in ["new", "in progress", "completed"]:
        print("Status must be one of: new, in progress, done")
        return []
    query = f" SELECT t.id, t.title, s.name FROM tasks t INNER JOIN status s ON t.status_id = s.id WHERE s.name = '{status}';"
    return execute_query(query)


def task3(task_id, new_status):
    """
    Оновити статус конкретного завдання. Змініть статус конкретного завдання на 'in progress' або інший статус.
    """
    if new_status not in ["new", "in progress", "completed"]:
        print("Status must be one of: new, in progress, done")
        return []
    to_change_query(
        "UPDATE tasks SET status_id = (SELECT id FROM status WHERE name = %s) WHERE id = %s;",
        (new_status, task_id),
    )


def task4():
    """Отримати список користувачів, які не мають жодного завдання. Використайте комбінацію SELECT, WHERE NOT IN і підзапит."""
    query = """
            SELECT * FROM users 
            WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks);
        """
    return execute_query(query)


def task5(user_id, title, description, status_id=1):
    """Додати нове завдання для конкретного користувача. Використайте INSERT для додавання нового завдання"""
    to_change_query(
        "INSERT INTO tasks (title, description, user_id, status_id) VALUES (%s, %s, %s, %s);",
        (title, description, user_id, status_id),
    )


def task6():
    """Отримати всі завдання, які ще не завершено. Виберіть завдання, чий статус не є 'завершено'."""
    query = """
            SELECT tasks.*
            FROM tasks
            JOIN status ON tasks.status_id = status.id
            WHERE status.name <> 'completed';
        """
    return execute_query(query)


def task7(id):
    """Видалити конкретне завдання. Використайте DELETE для видалення завдання за його id."""
    to_change_query("DELETE FROM tasks WHERE id = %s;", (id,))


def task8(pattern):
    """Знайти користувачів з певною електронною поштою. Використайте SELECT із умовою LIKE для фільтрації за електронною поштою."""
    query = f"""
            SELECT *
            FROM users
            WHERE email LIKE '%{pattern}%';
        """
    return execute_query(query)


def task9(user_id, name):
    """Оновити ім'я користувача. Змініть ім'я користувача за допомогою UPDATE"""
    to_change_query("UPDATE users SET fullname = %s WHERE id = %s;", (name, user_id))


def task10():
    """Отримати кількість завдань для кожного статусу. Використайте SELECT, COUNT, GROUP BY для групування завдань за статусами."""
    query = """
            SELECT status.name, COUNT(tasks.id) AS tasks_count
            FROM tasks
            JOIN status ON tasks.status_id = status.id
            GROUP BY status.name
            ORDER BY tasks_count DESC;
        """
    return execute_query(query)


def task11(pattern):
    """Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти.
    Використайте SELECT з умовою LIKE в поєднанні з JOIN, щоб вибрати завдання, призначені користувачам, чия електронна пошта містить певний домен (наприклад, '%@example.com').
    """
    query = """
            SELECT tasks.*
            FROM tasks
            JOIN users ON tasks.user_id = users.id
            WHERE users.email LIKE '{pattern}';
        """.format(
        pattern=pattern
    )
    return execute_query(query)


def task12():
    """Отримати список завдань, що не мають опису. Виберіть завдання, у яких відсутній опис"""
    queery = """
            SELECT *
            FROM tasks
            WHERE description IS NULL;
        """
    return execute_query(queery)


def task13():
    """Вибрати користувачів та їхні завдання, які є у статусі 'in progress'. Використайте INNER JOIN для отримання списку користувачів та їхніх завдань із певним статусом."""
    query = """
            SELECT users.fullname, tasks.title
            FROM users
            INNER JOIN tasks ON users.id = tasks.user_id
            WHERE tasks.status_id = (SELECT id FROM status WHERE name = 'in progress');
        """
    return execute_query(query)


def task14():
    """Отримати користувачів та кількість їхніх завдань. Використайте LEFT JOIN та GROUP BY для вибору користувачів та підрахунку їхніх завдань."""
    query = """
            SELECT users.fullname, COUNT(tasks.id) AS tasks_count
            FROM users
            LEFT JOIN tasks ON users.id = tasks.user_id
            GROUP BY users.fullname
            ORDER BY tasks_count DESC;
        """
    return execute_query(query)


if __name__ == "__main__":
    print(task14())
