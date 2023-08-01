import asyncio
import logging

from aiogram import Dispatcher

from tools.Bot import botInstance
from tools import bot_commands

from handlers import default_commands, group_commands, messages


async def main() -> None:
    dp = Dispatcher()
    dp.include_routers(group_commands.router, default_commands.router, messages.router)
    await bot_commands.check_commands()
    await dp.start_polling(botInstance)


if __name__ == '__main__':
    print('\n') #новая строка для предотвращения пересечения строк после перезапуска бота
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())