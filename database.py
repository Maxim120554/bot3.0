import sqlite3 as sq
from aiogram import types


def start_sql():
    global base, cur
    base = sq.connect('database.db')
    cur = base.cursor()
    if base:
        print('DB connected OK')
    else:
        print('noooo')
    base.execute("""CREATE TABLE IF NOT EXISTS users(
                    user_id PRIMARY KEY, 
                    user_name TEXT,
                    favorites TEXT)
                """)
    base.commit()


async def sql_add_command(message: types.Message):
    try:
        cur.execute('INSERT INTO users(user_id, user_name) VALUES(?, ?)', (message.from_user.id, message.from_user.first_name))
        base.commit()
    except sq.IntegrityError:
        pass






