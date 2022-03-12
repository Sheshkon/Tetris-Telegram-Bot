from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from config import URL_GAME_SITE


open_key = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Open site", url=URL_GAME_SITE)
        ]
    ],
)
