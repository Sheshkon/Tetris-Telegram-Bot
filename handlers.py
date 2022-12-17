import os.path
from uuid import uuid4

from aiogram import types
from aiogram.types import Message, InlineQueryResultGame
from aiogram.dispatcher.filters import Command

from keyboards import site_key, web_tetris_key
from exel import create_exel, delete_file
from main import bot, dp
from config import ADMINS_ID, RULES_TEXT, HELP_TEXT, START_TEXT, ABOUT_TEXT, SCREENSHOTS_LINKS, GAME_URLS, \
    GAME_SHORT_NAMES, RULES_PHOTO, START_GIF
from db import add_to_users_db, add_to_chats_db, get_all_id, get_all_users, get_leaderboard, add_to_leaderboard
from rsa_decrypt import decrypt, decode
from logger import save_log
from services import get_user_info, get_chat_info, send_game_request


@dp.callback_query_handler(lambda cq: cq.game_short_name in GAME_SHORT_NAMES)
async def send_welcome(cq: types.CallbackQuery):
    await bot.answer_callback_query(cq.id, url=GAME_URLS[GAME_SHORT_NAMES.index(cq.game_short_name)])


@dp.inline_handler()
async def send_game(inline_query: types.InlineQuery):
    r = []
    for i, game in enumerate(GAME_SHORT_NAMES):
        if inline_query.query in game:
            r.append(InlineQueryResultGame(id=str(uuid4()), game_short_name=GAME_SHORT_NAMES[i]))

    await bot.answer_inline_query(inline_query.id, r)


@dp.message_handler(Command('site'))
async def show(message: Message):
    await types.ChatActions.typing()
    await message.answer(text='On this website you can download the game', reply_markup=site_key)
    await save_log(msg=message)


@dp.message_handler(Command('web'))
async def show(message: Message):
    await types.ChatActions.typing()
    await message.answer(text='web version of the game', reply_markup=web_tetris_key)
    await save_log(msg=message)


@dp.message_handler(Command('start'))
async def send_welcome(message: Message):
    user_id, user_name, user_surname, user_nickname = get_user_info(message)
    chat_id, chat_name, chat_surname, chat_nickname, chat_full_name = get_chat_info(message)

    await add_to_users_db(user_id, user_name, user_surname, user_nickname)
    await add_to_chats_db(chat_id, chat_name, chat_surname, chat_nickname, chat_full_name)
    await save_log(msg=message)

    if 'iwannaplay' in message.text:
        await send_game_request(message, user_id, user_name, user_nickname)
    else:
        await message.answer(START_TEXT)
        await message.answer_animation(animation=START_GIF, caption='Example of the game')


@dp.message_handler(Command('send_all'))
async def send_all(message: Message):
    await types.ChatActions.typing()

    if message.from_user.id in ADMINS_ID:
        await message.answer('start')
        users = get_all_id("user_id", "users")
        await save_log(msg=message)
        for user in users:
            try:
                await types.ChatActions.typing()
                await bot.send_message(user, message.text[message.text.find(' '):])
                await save_log(text=f'message was sent to {user}')
            except:
                await save_log(text=f'skip user: {user}')
                continue
        await message.answer('done')
    else:
        await message.answer('error')


@dp.message_handler(Command('help'))
async def show_help(message: Message):
    await types.ChatActions.typing()
    await message.answer(HELP_TEXT)
    await save_log(msg=message)


@dp.message_handler(Command('rules'))
async def show_rules(message: Message):
    await types.ChatActions.typing()
    await message.answer(RULES_TEXT, parse_mode='HTML')
    await message.answer_photo(RULES_PHOTO)
    await save_log(msg=message)


@dp.message_handler(Command('about'))
async def show_rules(message: Message):
    await types.ChatActions.typing()
    await message.answer(ABOUT_TEXT, parse_mode='HTML')
    await save_log(msg=message)


@dp.message_handler(Command('get_all'))
async def show_all_users(message: Message):
    if message.from_user.id not in ADMINS_ID:
        return
    users = get_all_users('users')
    chats = get_all_users('chats')
    file_path = create_exel(users, chats)
    file = open(file_path, 'rb')
    await types.ChatActions.upload_document()
    await message.answer_document(file)
    await save_log(msg=message)

    while os.path.exists(file_path):
        try:
            delete_file(file_path)
        except:
            continue


@dp.message_handler(Command('screenshots'))
async def show_screens(message: Message):
    await types.ChatActions.upload_photo()

    media = types.MediaGroup()

    for screenshot in SCREENSHOTS_LINKS:
        media.attach_photo(screenshot)

    await message.answer_media_group(media)
    await save_log(msg=message)


@dp.message_handler(Command('decrypt'))
async def decrypt_message(message: Message):
    await types.ChatActions.typing()

    encrypted_msg = message.text[message.text.find(' '):]
    decrypted_msg = decrypt(encrypted_msg)

    await message.answer(decrypted_msg)
    await save_log(msg=message)


@dp.message_handler(Command('test'))
async def test_message(message: Message):
    await bot.send_message(ADMINS_ID[1], message.text[message.text.find(' '):])
    await save_log(msg=message)


@dp.message_handler(Command('leaderboard'))
async def show_leaderboard(message: Message):
    leaderboard = get_leaderboard()
    for game in leaderboard:
        await types.ChatActions.typing()
        await message.answer(game)
    await save_log(msg=message)


@dp.message_handler(Command('add_score'))
async def add_score(message: Message):
    try:
        await save_log(msg=message)
        encrypted_msg = message.text[message.text.find(' '):]
        # decrypted_msg = decrypt(encrypted_msg)
        decrypted_msg = decode(encrypted_msg)
        await save_log(text=f'decode string: {decrypted_msg}')
        nickname = f'@{message.from_user.username}' if message.from_user.username else message.from_user.first_name
        await add_to_leaderboard(message.from_user.id, nickname, decrypted_msg.split())
    except:
        await save_log(text=f'add_score error, command: {message.text}')
        await message.answer('invalid score')


@dp.message_handler(Command('get_latest_update'))
async def get_latest_update(message: Message):
    await save_log(msg=message)
    await types.ChatActions.typing()
    try:
        with open('latest_version/update.txt', encoding='utf8') as f:
            update_text = f.read()
        await message.answer_photo(photo=open('latest_version/update.png', 'rb'), caption=update_text)
    except:
        await save_log(text='get latest update error')


@dp.message_handler(Command('send_update'))
async def send_update(message: Message):
    await save_log(msg=message)
    await types.ChatActions.typing()

    if message.from_user.id in ADMINS_ID:
        try:
            with open('latest_version/update.txt', encoding='utf8') as f:
                update_text = f.read()
        except:
            await message.answer("no update file")
            await save_log(text="no update file")

        users = get_all_id("user_id", "users")
        update_message = await bot.send_photo(message.from_user.id, photo=open('latest_version/update.png', 'rb'),
                                              caption=update_text)
        log = ''
        for user in users:
            try:
                log += f'update was sent to {user}\n'
                await update_message.send_copy(user)
                # await save_log(text=f'update was sent to {user}')
            except:
                log += f'skip user: {user}\n'
                # await save_log(text=f'skip user: {user}')
                continue

        await save_log(text=log)


@dp.message_handler(Command('send_tip'))
async def send_tip(message: Message):
    await save_log(msg=message)
    await types.ChatActions.typing()

    if message.from_user.id in ADMINS_ID:
        try:
            with open('tips/txt/tip1.txt', encoding='utf8') as f:
                tip_text = f.read()
        except:
            await message.answer("no tips")
            await save_log(text="no tips")

        tip_message = await bot.send_photo(message.from_user.id, photo=open('tips/img/tip1.png', 'rb'),
                                           caption=tip_text)
        users = get_all_id("user_id", "users")
        for user in users:
            try:
                await tip_message.send_copy(user)
                await save_log(text=f'tip was sent to {user}')
            except:
                await save_log(text=f'skip user: {user}')
                continue
