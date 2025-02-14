import asyncio
import logging

from aiogram import Dispatcher

from tools.Bot import botInstance
from tools import bot_commands

from handlers import default_commands
from handlers.group_monitor import group_commands, group_messages
from handlers.private_group_registration import *


async def main() -> None:
    dp = Dispatcher()
    dp.include_routers(group_commands.router, default_commands.router, group_messages.router)
    await bot_commands.check_commands()
    await dp.start_polling(botInstance)


if __name__ == '__main__':
    print('\n') #новая строка для предотвращения пересечения строк после перезапуска бота
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())