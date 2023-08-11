import os
from dotenv import load_dotenv
import psycopg2


load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
user = "postgres"
password = "qwer"
db_name = 'exam_bot'
host = '127.0.0.1'


try:
    # Подключаемся к базе данных
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    connection.autocommit = True

    # Создаём курсор для того, чтобы выполнять операции с базой
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT version();"
        )
        print(f"Server version: {cursor.fetchone()}")
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users (
            id INT PRIMARY KEY);"""
        )
except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    pass


