from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from config import URL_GAME_SITE, URL_WEB_GAME


site_key = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Open site", url=URL_GAME_SITE)
        ]
    ],
)

web_tetris_key = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("play", url=URL_WEB_GAME)
        ]
    ],
)
