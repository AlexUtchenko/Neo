"""
DAG: підрахунок медалей з розгалуженням, затримкою та SQL-сенсором.

create_table -> pick_medal -> pick_medal_task -> [calc_Bronze | calc_Silver | calc_Gold]
             -> generate_delay -> check_for_correctness
"""
import random
import time
from datetime import datetime

from airflow import DAG
from airflow.operators.python import BranchPythonOperator, PythonOperator
from airflow.providers.common.sql.sensors.sql import SqlSensor
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.utils.trigger_rule import TriggerRule

# ---- налаштування (заміни на свої) ----------------------------------------
CONN_ID = "goit_mysql_db"                       # Airflow Connection до MySQL
TABLE = "olympic_dataset.oleksaut_medal_counts" # схема.таблиця для результатів
SOURCE = "olympic_dataset.athlete_event_results"
MEDALS = ["Bronze", "Silver", "Gold"]
FRESHNESS_SEC = 30                              # макс. "вік" останнього запису
# ---------------------------------------------------------------------------


def _pick_medal() -> str:
    medal = random.choice(MEDALS)
    print(f"Обрано медаль: {medal}")
    return medal                                # -> XCom (return_value)


def _branch(ti) -> str:
    medal = ti.xcom_pull(task_ids="pick_medal")
    return f"calc_{medal}"                      # task_id гілки, що виконається


def _generate_delay(seconds) -> None:
    seconds = int(seconds)
    print(f"Затримка {seconds} с")
    time.sleep(seconds)


with DAG(
    dag_id="oleksaut_medal_count",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    # delay можна змінити при ручному запуску: Trigger DAG w/ config -> {"delay": 35}
    params={"delay": 5},
    tags=["oleksaut", "medals"],
) as dag:

    # 1. Таблиця для результатів
    create_table = SQLExecuteQueryOperator(
        task_id="create_table",
        conn_id=CONN_ID,
        sql=f"""
        CREATE TABLE IF NOT EXISTS {TABLE} (
            id          INT AUTO_INCREMENT PRIMARY KEY,
            medal_type  VARCHAR(10) NOT NULL,
            `count`     INT NOT NULL,
            created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """,
    )

    # 2. Випадковий вибір медалі
    pick_medal = PythonOperator(
        task_id="pick_medal",
        python_callable=_pick_medal,
    )

    # 3. Розгалуження
    pick_medal_task = BranchPythonOperator(
        task_id="pick_medal_task",
        python_callable=_branch,
    )

    # 4. Три гілки підрахунку (COUNT + запис в одному INSERT ... SELECT)
    calc_tasks = [
        SQLExecuteQueryOperator(
            task_id=f"calc_{medal}",
            conn_id=CONN_ID,
            sql=f"""
            INSERT INTO {TABLE} (medal_type, `count`, created_at)
            SELECT '{medal}', COUNT(*), NOW()
            FROM {SOURCE}
            WHERE medal = '{medal}';
            """,
        )
        for medal in MEDALS
    ]

    # 5. Затримка: запускається, якщо хоча б одна гілка успішна
    #    (дві інші гілки skipped -> дефолтний all_success тут не підходить)
    generate_delay = PythonOperator(
        task_id="generate_delay",
        python_callable=_generate_delay,
        op_kwargs={"seconds": "{{ params.delay }}"},
        trigger_rule=TriggerRule.ONE_SUCCESS,
    )

    # 6. Сенсор: найновіший запис не старший за 30 с.
    #    Порівняння робиться на боці MySQL (NOW() vs created_at) — один годинник,
    #    без проблем із часовими поясами між Airflow та БД.
    #    SqlSensor успішний, коли перша клітинка результату "truthy" (1).
    check_for_correctness = SqlSensor(
        task_id="check_for_correctness",
        conn_id=CONN_ID,
        sql=f"""
        SELECT TIMESTAMPDIFF(SECOND, MAX(created_at), NOW()) <= {FRESHNESS_SEC}
        FROM {TABLE};
        """,
        mode="poke",
        poke_interval=5,
        timeout=20,          # запис лише старішає, тож довго чекати сенсу немає
        fail_on_empty=False,
    )

    (
        create_table
        >> pick_medal
        >> pick_medal_task
        >> calc_tasks
        >> generate_delay
        >> check_for_correctness
    )
