import sqlite3
import os

def execute_sql_command(sql_command, db_path='site.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.executescript(sql_command)

    conn.commit()
    conn.close()

def init_db():
    sql_folder = os.path.join('sql_files')

    with open(os.path.join(sql_folder, 'user.sql'), 'r') as file:
        sql_command_user = file.read()
        execute_sql_command(sql_command_user)

    with open(os.path.join(sql_folder, 'random_prices.sql'), 'r') as file:
        sql_command_food = file.read()
        execute_sql_command(sql_command_food)

if __name__ == '__main__':
    init_db()

