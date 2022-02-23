import psycopg2
from config import DB_URI

conn = psycopg2.connect(DB_URI, sslmode='require')
cursor = conn.cursor()


async def add_to_users_db(user_id: int, user_name: str, user_surname: str, user_nickname: str):
    cursor.execute(f'SELECT user_id FROM users WHERE user_id = {user_id}')
    result = cursor.fetchone()
    if not result:
        cursor.execute('INSERT INTO users (user_id, user_name, user_surname, user_nickname) VALUES (%s, %s, %s, %s)',
                       (user_id, user_name, user_surname, user_nickname))
    conn.commit()


async def add_to_chats_db(chat_id: int, chat_name: str, chat_surname: str, chat_nickname: str, chat_full_name: str):
    if chat_id > 0:
        return
    cursor.execute(f'SELECT chat_id FROM chats WHERE chat_id = {chat_id}')
    result = cursor.fetchone()
    if not result:
        cursor.execute('INSERT INTO chats (chat_id, chat_name, chat_surname, chat_nickname, chat_full_name) VALUES (%s, %s, %s, %s, %s)',
                       (chat_id, chat_name, chat_surname, chat_nickname, chat_full_name))
    conn.commit()


async def get_all_id(name_id: str, table: str):
    cursor.execute(f'SELECT {name_id} FROM {table}')
    result = cursor.fetchall()
    return [i[0] for i in result]


async def get_all_users(table: str):
    cursor.execute(f'SELECT * FROM {table}')
    result = cursor.fetchall()
    return result
