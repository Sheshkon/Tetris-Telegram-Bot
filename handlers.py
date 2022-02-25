from asyncio import sleep, create_task
from contextlib import suppress
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Command
from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound
from keyboards import open_key
from exel import create_exel, delete_file
from main import bot, dp
from config import ADMINS_ID, RULES_TEXT, HELP_TEXT, START_TEXT, ABOUT_TEXT, SCREENSHOTS_LINKS, URL_GAME_SITE
from db import add_to_users_db, add_to_chats_db, get_all_id, get_all_users, get_user_id, get_chat_id, get_user_db_id, get_chat_db_id
from rsa_decrypt import decrypt


async def restart_server(dp):
    for admin in ADMINS_ID:
        await bot.send_message(admin, text='Restart server &#127758;')


async def delete_message(message: Message, sleep_time: int = 0):
    await sleep(sleep_time)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await message.delete()


@dp.message_handler(Command('site'))
async def show(message: Message):
    await message.answer(text='In this site you can download the game', reply_markup=open_key)


async def get_user_info(msg: Message):
    return msg.from_user.id, msg.from_user.first_name, msg.from_user.last_name, msg.from_user.username


async def get_chat_info(msg: Message):
    return msg.chat.id, msg.chat.first_name, msg.chat.last_name, msg.chat.username, msg.chat.full_name


def get_data(msg: Message):
    data = msg.text.split('=')

    room, opponent = data[1], data[2]
    if opponent == 'all':
        return room, opponent

    opponent = int(opponent)
    opponent_id = get_user_id(opponent) if opponent > 0 else get_chat_id(abs(opponent))

    print(opponent_id)

    return room, opponent_id


@dp.message_handler(Command('start'))
async def send_welcome(message: Message):
    user_id, user_name, user_surname, user_nickname = await get_user_info(message)
    chat_id, chat_name, chat_surname, chat_nickname, chat_full_name = await get_chat_info(message)

    await add_to_users_db(user_id, user_name, user_surname, user_nickname)
    await add_to_chats_db(chat_id, chat_name, chat_surname, chat_nickname, chat_full_name)
    # await message.answer(message.text)

    if 'iwannaplay' in message.text:
        room, opponent = get_data(message)

        users = await get_all_id("user_id", "users") if opponent == 'all' else [opponent]
        # groups = await(get_all_id("chat_id", "chats"))
        # users += groups

        play_key = InlineKeyboardMarkup()
        username_request, name_request = message.from_user.username, message.from_user.first_name
        nickname_request = username_request if username_request else name_request
        opponent = get_user_db_id(message.from_user.id)

        play_key.add(InlineKeyboardButton('Play!', url=URL_GAME_SITE + f'?room={room}&opponent={opponent}'))
        for user in users:
            if user != user_id:
                try:
                    msg = await bot.send_message(user, f'{nickname_request}\nWho wanna play with me?',
                                                 reply_markup=play_key)
                    create_task(delete_message(msg, 60))
                except:
                    continue

        await message.answer('request was sent')

    else:
        await message.answer(START_TEXT)
        await message.answer_animation(
            animation='https://raw.githubusercontent.com/vitaliysheshkoff/Tetris-Multiplayer/main/screenshots/play.gif')


@dp.message_handler(Command('sendall'))
async def send_all(message: Message):
    if message.chat.id in ADMINS_ID:
        await message.answer('start')
        users = await get_all_id("user_id", "users")
        for user in users:
            try:
                await bot.send_message(user, message.text[message.text.find(' '):])
            except:
                continue

        await message.answer('done')

    else:
        await message.answer('error')


@dp.message_handler(Command('help'))
async def show_help(message: Message):
    await message.answer(HELP_TEXT)


@dp.message_handler(Command('rules'))
async def show_rules(message: Message):
    await message.answer(RULES_TEXT, parse_mode='HTML')
    await message.answer_photo(
        'https://github.com/vitaliysheshkoff/Tetris-Multiplayer/raw/main/screenshots/image_2021-09-12_11-25-36.png')


@dp.message_handler(Command('about'))
async def show_rules(message: Message):
    await message.answer(ABOUT_TEXT, parse_mode='HTML')


@dp.message_handler(Command('getall'))
async def show_all_users(message: Message):
    if message.chat.id in ADMINS_ID:
        users = await get_all_users("users")
        file_path = await create_exel(users)
        await message.answer_document(open(file_path, "rb"))
        await delete_file(file_path)


@dp.message_handler(Command('screenshots'))
async def show_screens(message: Message):
    for screenshot in SCREENSHOTS_LINKS:
        await message.answer_photo(screenshot)


# @dp.message_handler(
#     content_types=['document', 'text', 'audio', 'photo', 'sticker', 'video', 'video_note', 'voice', 'location',
#                    'contact'])
# async def send_file(message: Message):
#     if message.chat.id in ADMINS_ID:
#         users = await get_all_id("user_id", "users")
#         for user in users:
#             await bot.forward_message(user, message.chat.id, message.message_id)


@dp.message_handler(Command('decrypt'))
async def show_screens(message: Message):
    encrypted_msg = message.text[message.text.find(' '):]
    decrypted_msg = await decrypt(encrypted_msg)
    await message.answer(decrypted_msg)
