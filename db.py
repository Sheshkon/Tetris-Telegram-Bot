import psycopg2
from config import DB_URI
from logger import save_log
from main import bot
from services import is_valid_score

conn = psycopg2.connect(DB_URI, sslmode='require')
cursor = conn.cursor()


async def add_to_users_db(user_id: int, user_name: str, user_surname: str, user_nickname: str):
    cursor.execute(f'SELECT user_id FROM users WHERE user_id = {user_id}')
    result = cursor.fetchone()
    if not result:
        cursor.execute('INSERT INTO users (user_id, user_name, user_surname, user_nickname) VALUES (%s, %s, %s, %s)',
                       (user_id, user_name, user_surname, user_nickname))
        log_text = f'adding to db: {user_id, user_name, user_surname, user_nickname}'
    else:
        cursor.execute('UPDATE users SET user_name=%s, user_surname=%s, user_nickname=%s WHERE user_id=%s',
                       (user_name, user_surname, user_nickname, user_id))
        log_text = f'updating db: {user_id, user_name, user_surname, user_nickname}'

    conn.commit()

    await save_log(text=log_text)


async def add_to_chats_db(chat_id: int, chat_name: str, chat_surname: str, chat_nickname: str, chat_full_name: str):
    if chat_id > 0:
        return

    cursor.execute(f'SELECT chat_id FROM chats WHERE chat_id = {chat_id}')
    result = cursor.fetchone()
    if not result:
        cursor.execute(
            'INSERT INTO chats (chat_id, chat_name, chat_surname, chat_nickname, chat_full_name) VALUES (%s, %s, %s, %s, %s)',
            (chat_id, chat_name, chat_surname, chat_nickname, chat_full_name))
    conn.commit()

    await save_log(text=f'adding to db: {chat_id, chat_name, chat_surname, chat_nickname, chat_full_name}')


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
    cursor.execute(f'SELECT * FROM leaderboard ORDER BY score DESC LIMIT 3')
    result = cursor.fetchall()
    leaderboard = [f'{i + 1}:\nnickname: {data[0].rstrip()}\nscore:{data[1]}\n' \
                   f'lvl: {data[2]}\ndate: {data[3].rstrip()}'
                   for i, data in enumerate(result)]
    leaderboard.append('\nfull leaderboard you can find on website (use /site)')

    return leaderboard


async def add_to_leaderboard(user_id, nickname, data):
    await save_log(text=data)
    is_valid, error = is_valid_score(data)
    if not is_valid:
        await save_log(text=f'{user_id, nickname}: invalid score ({error})')
        return

    cursor.execute(f'SELECT score FROM leaderboard WHERE id={user_id}')
    result = cursor.fetchone()

    if result:
        if result[0] >= int(data[0]):
            await bot.send_message(user_id, 'your current score is not higher than the previously published one')
            await save_log(text=f'{user_id, nickname}: your current score is not higher than the previously published one')
            return

        cursor.execute('UPDATE leaderboard SET nickname=%s, score=%s, lvl=%s, game_date=%s WHERE id=%s',
                       (nickname, int(data[0]), int(data[1]), data[2], user_id))
        conn.commit()

        await bot.send_message(user_id, 'leaderboard updated')
        await save_log(text=f'{user_id, nickname}: leaderboard updated')
        return

    cursor.execute(
        'INSERT INTO leaderboard (nickname, score, lvl, game_date, id) VALUES (%s, %s, %s, %s, %s)',
        (nickname, int(data[0]), int(data[1]), data[2], user_id))
    conn.commit()

    await bot.send_message(user_id, f'added to leaderboard {nickname, data[0], data[1], data[2]}')
    await save_log(text=f'added to leaderboard [{nickname}: {data}]')
