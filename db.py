import psycopg2
from config import DB_URI

conn = psycopg2.connect(DB_URI, sslmode='require')
cursor = conn.cursor()


def add_to_users_db(user_id: int, user_name: str, user_surname: str, user_nickname: str):
    cursor.execute(f'SELECT user_id FROM users WHERE user_id = {user_id}')
    result = cursor.fetchone()
    if not result:
        cursor.execute('INSERT INTO users (user_id, user_name, user_surname, user_nickname) VALUES (%s, %s, %s, %s)',
                       (user_id, user_name, user_surname, user_nickname))
        print(f'adding to db: {user_id, user_name, user_surname, user_nickname}')
    else:
        cursor.execute('UPDATE users SET user_name=%s, user_surname=%s, user_nickname=%s WHERE user_id=%s',
                       (user_name, user_surname, user_nickname, user_id))
        print(f'updating db: {user_id, user_name, user_surname, user_nickname}')

    conn.commit()


def add_to_chats_db(chat_id: int, chat_name: str, chat_surname: str, chat_nickname: str, chat_full_name: str):
    if chat_id > 0:
        return
    cursor.execute(f'SELECT chat_id FROM chats WHERE chat_id = {chat_id}')
    result = cursor.fetchone()
    if not result:
        cursor.execute(
            'INSERT INTO chats (chat_id, chat_name, chat_surname, chat_nickname, chat_full_name) VALUES (%s, %s, %s, %s, %s)',
            (chat_id, chat_name, chat_surname, chat_nickname, chat_full_name))
        print(f'adding to db: {chat_id, chat_name, chat_surname, chat_nickname, chat_full_name}')
    conn.commit()


def get_all_id(name_id: str, table: str):
    cursor.execute(f'SELECT {name_id} FROM {table}')
    result = cursor.fetchall()
    return [i[0] for i in result]


def get_all_users(table: str):
    cursor.execute(f'SELECT * FROM {table}')
    result = cursor.fetchall()
    return result


def get_user_id(user_db_id):
    cursor.execute(f'SELECT user_id FROM users WHERE user_db_id = {user_db_id}')
    result = cursor.fetchone()
    return result[0]


def get_chat_id(chat_db_id):
    cursor.execute(f'SELECT chat_id FROM chats WHERE chat_db_id = {chat_db_id}')
    result = cursor.fetchone()
    return result[0]


def get_user_db_id(user_id):
    cursor.execute(f'SELECT user_db_id FROM users WHERE user_id = {user_id}')
    result = cursor.fetchone()
    return result[0]


def get_chat_db_id(chat_id):
    cursor.execute(f'SELECT chat_db_id FROM chats WHERE chat_id = {chat_id}')
    result = cursor.fetchone()
    return result[0]


def get_leaderboard():
    cursor.execute(f'SELECT * FROM leaderboard ORDER BY score DESC')
    result = cursor.fetchall()
    leaderboard = (f'{i + 1}:\nnickname: {data[0].rstrip()}\nscore:{data[1]}\n' \
                   f'date: {data[2].rstrip()}\nplay time: {data[3].rstrip()}'
                   for i, data in enumerate(result))
    return leaderboard
