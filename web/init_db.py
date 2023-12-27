import sqlite3
import os

def execute_sql_command(sql_command, db_path='instance/site.db'):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Execute the SQL command
    cursor.executescript(sql_command)

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

def init_db():
    # Load SQL files
    sql_folder = os.path.join('instance', 'sqlFiles')

    # Execute user.sql
    with open(os.path.join(sql_folder, 'user.sql'), 'r') as file:
        sql_command_user = file.read()
        execute_sql_command(sql_command_user)

    # Execute food.sql
    with open(os.path.join(sql_folder, 'food.sql'), 'r') as file:
        sql_command_food = file.read()
        execute_sql_command(sql_command_food)

if __name__ == '__main__':
    init_db()
