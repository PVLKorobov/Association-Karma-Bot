from aiogram import Bot
from aiogram.utils.token import TokenValidationError

import os, sys

from tools import config_handler, bot_commands


def restart_bot():
    print('RESTARTING BOT')
    os.execl(sys.executable, f'"{sys.executable}"', *sys.argv)

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


while True:
    try:
        botInstance = Bot(config_handler.get_param('accessToken'), parse_mode="HTML")
        break
    except TokenValidationError:
        print('Был введён недействительный токен.')
        config_handler.new_token()
        clear_terminal()
        restart_bot()