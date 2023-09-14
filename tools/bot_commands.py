from aiogram import types

from tools.Bot import botInstance


async def set_bot_commands() -> None:
    dafaultCommands = [
        types.BotCommand(command='/myscore', description='Узнать свой счёт'),
        types.BotCommand(command='/help', description='Список доступных команд')
    ]
    await botInstance.set_my_commands(dafaultCommands, scope=types.BotCommandScopeDefault())

    groupAdminCommands = [
        types.BotCommand(command='/help', description='Список доступных команд'),
        types.BotCommand(command='/myscore', description='Узнать свой счёт'),
        types.BotCommand(command='/listscore', description='Вывести счёт всех пользователей'),
        types.BotCommand(command='/reset', description='Очистить сохранённые данные'),
        types.BotCommand(command='/resetconfig', description='Сбросить настройки бота'),
        types.BotCommand(command='/settoken', description='Сменить код доступа бота'),
        types.BotCommand(command='/reloadcommands', description="Сбросить меню комманд бота"),
        types.BotCommand(command='/status', description='Техническая информация бота'),
        types.BotCommand(command='/silent', description='Переключение тихого режима'),
        types.BotCommand(command='/silenttimer', description='Установить задержку в тихом режиме'),
        types.BotCommand(command='/setscore', description='Установить сколько баллов начисляет бот'), 
        types.BotCommand(command='/setscorename', description='Установить название баллов'),
        types.BotCommand(command='/addscore', description='Добавить баллы пользователю'),
        types.BotCommand(command='/setscorename', description='Установить шаблон поиска')
    ]
    await botInstance.set_my_commands(groupAdminCommands, types.BotCommandScopeAllChatAdministrators())


async def check_commands() -> None:
    commandsList = await botInstance.get_my_commands(types.BotCommandScopeDefault()) + await botInstance.get_my_commands(types.BotCommandScopeAllChatAdministrators())
    if len(commandsList) == 0:
        set_bot_commands()