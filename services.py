from asyncio import sleep, create_task

from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import exceptions
from contextlib import suppress

from config import ADMINS_ID, URL_GAME_SITE
from logger import save_log
from main import bot, dp
from rsa_decrypt import encode
import db


async def restart_server(dp):
    for admin in ADMINS_ID:
        msg = await bot.send_message(admin, text='Restart server &#127758;')

    await save_log(msg=msg)


async def delete_message(message: Message, sleep_time: int = 0):
    await sleep(sleep_time)
    with suppress(exceptions.MessageCantBeDeleted, exceptions.MessageToDeleteNotFound):
        await message.delete()


async def send_game_request(msg: Message, sender_id, sender_name, sender_username):
    room, opponent = get_data(msg)
    users = db.get_all_id("user_id", "users") if opponent == 'all' else [opponent]
    play_key = InlineKeyboardMarkup()
    player = f'{sender_name}({sender_username})' if sender_username else f'{sender_name}()'
    encode_player = await encode(player)
    play_key.add(InlineKeyboardButton('Play!', url=URL_GAME_SITE + f'?room={room}&opponent={encode_player}'))

    await save_log(text=f'users: {users}, sender_id: {sender_id}')

    for user in users:
        if user != sender_id:
            try:
                request_msg = await bot.send_message(user, f'{player}:\nDo you wanna play with me?',
                                                     reply_markup=play_key, parse_mode='None')
                create_task(delete_message(request_msg, 120))
                await save_log(text=f'request was sent to {user}')
            except:
                await save_log(text=f'skip user: {user}')
                continue

    await msg.answer('request was sent')


def get_user_info(msg: Message):
    return msg.from_user.id, msg.from_user.first_name, msg.from_user.last_name, msg.from_user.username


def get_chat_info(msg: Message):
    return msg.chat.id, msg.chat.first_name, msg.chat.last_name, msg.chat.username, msg.chat.full_name


def get_data(msg: Message):
    data = msg.text.split('=')
    room, opponent = data[1], data[2]

    if opponent == 'all':
        return room, opponent

    opponent = int(opponent)
    opponent_id = db.get_user_id(opponent) if opponent > 0 else db.get_chat_id(abs(opponent))

    return room, opponent_id


def is_valid_score(score):
    if len(score) != 3:
        return False, 'invalid length'

    if not (score[0].isdigit() and score[1].isdigit()):
        return False, 'invalid symbol in score or lvl'

    date = score[2].split('/')
    for number in date:
        if not (number.isdigit()):
            return False, 'invalid symbol in date'

    return True, ''
