from asyncio import sleep, create_task
from contextlib import suppress
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Command
from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound
from keyboards import open_key
from exel import create_exel, delete_file
from main import bot, dp
from config import ADMINS_ID, RULES_TEXT, HELP_TEXT, START_TEXT, ABOUT_TEXT, SCREENSHOTS_LINKS, URL_GAME_SITE
from db import add_to_users_db, add_to_chats_db, get_all_id, get_all_users, get_user_id, get_chat_id
from rsa_decrypt import decrypt, encode


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
    print(f'{message.from_user.id} command: {message.text}')


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
    opponent_id = get_user_id(opponent) if opponent > 0 else get_chat_id(abs(opponent))

    return room, opponent_id


async def send_game_request(msg: Message, sender_id, sender_name, sender_username):
    room, opponent = get_data(msg)
    users = get_all_id("user_id", "users") if opponent == 'all' else [opponent]
    # groups = (get_all_id("chat_id", "chats"))
    # users += groups

    play_key = InlineKeyboardMarkup()

    player = f'{sender_name}({sender_username})' if sender_username else f'{sender_name}()'
    encode_player = encode(player)

    play_key.add(InlineKeyboardButton('Play!', url=URL_GAME_SITE + f'?room={room}&opponent={encode_player}'))
    print("users: ", users, "user_id: ", sender_id)
    for user in users:
        if user != sender_id:
            try:
                msg = await bot.send_message(user, f'{player}:\nDo you wanna play with me?',
                                             reply_markup=play_key, parse_mode='None')
                create_task(delete_message(msg, 120))
                print(f'request was sent to {user}')
            except:
                print("skip user: ", user)
                continue

    await msg.answer('request was sent')

    pass


@dp.message_handler(Command('start'))
async def send_welcome(message: Message):
    user_id, user_name, user_surname, user_nickname = get_user_info(message)
    chat_id, chat_name, chat_surname, chat_nickname, chat_full_name = get_chat_info(message)

    add_to_users_db(user_id, user_name, user_surname, user_nickname)
    add_to_chats_db(chat_id, chat_name, chat_surname, chat_nickname, chat_full_name)
    print(f'{user_id, user_name, user_surname, user_nickname} command: {message.text}')

    if 'iwannaplay' in message.text:
        await send_game_request(message, user_id, user_name, user_nickname)

    else:
        await message.answer(START_TEXT)
        await message.answer_animation(
            animation='https://raw.githubusercontent.com/vitaliysheshkoff/Tetris-Multiplayer/main/screenshots/play.gif')


@dp.message_handler(Command('sendall'))
async def send_all(message: Message):
    if message.from_user.id in ADMINS_ID:
        await message.answer('start')
        users = get_all_id("user_id", "users")
        for user in users:
            try:
                await bot.send_message(user, message.text[message.text.find(' '):])
                print(f'message was sent to {user}')
            except:
                print("skip user: ", user)
                continue

        await message.answer('done')

    else:
        await message.answer('error')


@dp.message_handler(Command('help'))
async def show_help(message: Message):
    await message.answer(HELP_TEXT)
    print(f'{message.from_user.id} command: {message.text}')


@dp.message_handler(Command('rules'))
async def show_rules(message: Message):
    await message.answer(RULES_TEXT, parse_mode='HTML')
    await message.answer_photo(
        'https://github.com/vitaliysheshkoff/Tetris-Multiplayer/raw/main/screenshots/image_2021-09-12_11-25-36.png')
    print(f'{message.from_user.id} command: {message.text}')


@dp.message_handler(Command('about'))
async def show_rules(message: Message):
    await message.answer(ABOUT_TEXT, parse_mode='HTML')
    print(f'{message.from_user.id} command: {message.text}')


@dp.message_handler(Command('getall'))
async def show_all_users(message: Message):
    if message.from_user.id in ADMINS_ID:
        users = get_all_users("users")
        file_path = create_exel(users)
        await message.answer_document(open(file_path, "rb"))
        print(f'{message.from_user.id}: get all users')
        delete_file(file_path)


@dp.message_handler(Command('screenshots'))
async def show_screens(message: Message):
    for screenshot in SCREENSHOTS_LINKS:
        await message.answer_photo(screenshot)
        print(f'{message.from_user.id} command: {message.text}')


# @dp.message_handler(
#     content_types=['document', 'text', 'audio', 'photo', 'sticker', 'video', 'video_note', 'voice', 'location',
#                    'contact'])
# async def send_file(message: Message):
#     if message.from_user.id in ADMINS_ID:
#         users = get_all_id("user_id", "users")
#     for user in users:
#         try:
#             await bot.forward_message(user, message.chat.id, message.message_id)
#             print(f'message was sent to {user}')
#         except:
#             print("skip user: ", user)
#             continue


@dp.message_handler(Command('decrypt'))
async def show_screens(message: Message):
    print(f'{message.from_user.id} command: {message.text}')
    encrypted_msg = message.text[message.text.find(' '):]
    decrypted_msg = decrypt(encrypted_msg)
    await message.answer(decrypted_msg)


@dp.message_handler(Command('test'))
async def test_message(message: Message):
    await bot.send_message(ADMINS_ID[1], message.text[message.text.find(' '):])
    print(f'{message.from_user.id} command: {message.text}')

