from aiogram.types import Message
from main import bot
from config import LOG_ID


async def save_log(text: str = None, msg: Message = None):
    if msg:
        log_txt = f'[{msg.from_user.id, msg.from_user.username, msg.from_user.first_name}]'\
              f'\n command: {msg.text}'
    else:
        log_txt = text

    print(log_txt)
    await bot.send_message(LOG_ID, log_txt)