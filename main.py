import asyncio
from uuid import uuid4

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Command
from aiogram.types import InlineQueryResultGame

from config import BOT_TOKEN

loop = asyncio.new_event_loop()
bot = Bot(BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, loop=loop)


if __name__ == '__main__':
    from handlers import dp, restart_server
    executor.start_polling(dp, on_startup=restart_server)