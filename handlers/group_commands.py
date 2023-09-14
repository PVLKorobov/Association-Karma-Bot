from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from tools import config_handler, data_handler, bot_commands, strings
from tools.filters import ChatType, IsAdmin
from tools.Bot import botInstance, restart_bot


#global
router = Router()
#


@router.message(Command(commands=['help']), ChatType(chatType=['group', 'supergroup']), IsAdmin())
async def command_help(message: Message) -> None:
    responseText = data_handler.get_response_text('helpAdmin')
    await message.reply(responseText)


@router.message(Command(commands=['reloadcommands']), ChatType(chatType=['group', 'supergroup']), IsAdmin())
async def command_reload_commands(message: Message) -> None:
    await bot_commands.set_bot_commands()
    await message.reply('<b>Меню команд перезагружено!</b>')


@router.message(Command(commands=['resetconfig']), ChatType(chatType=['group', 'supergroup']), IsAdmin())
async def command_reset_config(message: Message) -> None:
    config_handler.create_config_file(new=False)
    await message.reply('<b>Настройки бота сброшены!\nБот будет перезапущен.</b>')
    restart_bot()
    


@router.message(Command(commands=['reset']), ChatType(chatType=['group', 'supergroup']), IsAdmin())
async def command_reset(message: Message) -> None:
    data_handler.create_data_file()
    await message.reply('<b>Данные бота сброшены!\nБот будет перезапущен.</b>')
    restart_bot()


@router.message(Command(commands=['settoken']), ChatType(chatType=['group', 'supergroup']), IsAdmin())
async def command_set_token(message: Message) -> None:
    await message.reply('<b>Введите новый код доступа в коммандной строке терминала бота</b>')
    config_handler.new_token()
    await message.reply('<b>Код доступа изменён!\nБот будет перезапущен.</b>')
    restart_bot()


@router.message(Command(commands=['listscore']), ChatType(chatType=['group', 'supergroup']), IsAdmin())
async def command_list_score(message: Message) -> None:
    scoreTable = data_handler.get_score_table()
    if len(scoreTable) > 0:
        responseText = data_handler.get_response_text('scoreList').format(scoreName=config_handler.get_param('scoreNames')['plural'], scoreTable=scoreTable)
    else:
        responseText = data_handler.get_response_text('scoreListFail').format(scoreName=config_handler.get_param('scoreNames')['mid'])
    await message.answer(responseText, disable_notification=True)


@router.message(Command(commands=['status']), ChatType(chatType=['group', 'supergroup']), IsAdmin())
async def commands_status(message: Message) -> None:
    bot = await botInstance.get_me()
    scoreNames = config_handler.get_param('scoreNames')
    replyText = data_handler.get_response_text('status').format(botName=bot.mention_html(), silentStatus=strings.get_param_state(data_handler.get_param('silentMode')), 
                                                                silentTime=config_handler.get_param('cacheTimeout'), 
                                                                scoreName=scoreNames['high'], 
                                                                addedScoreAmount=config_handler.get_param('addedScoreAmount'), 
                                                                lowName=scoreNames['low'], 
                                                                midName=scoreNames['mid'], 
                                                                highName=scoreNames['high'], 
                                                                pluralName=scoreNames['plural'])
    await message.answer(replyText, disable_notification=True)


@router.message(Command(commands=['silent']), ChatType(chatType=['group', 'supergroup']), IsAdmin())
async def command_silent_mode(message: Message) -> None:
    currentState = data_handler.get_param('silentMode')
    data_handler.set_param('silentMode', not currentState)
    await message.reply(f'Тихий режим <b>{strings.get_param_state(not currentState)}</b>')
    

@router.message(Command(commands=['silenttimer']), ChatType(chatType=['group', 'supergroup']), IsAdmin())
async def command_set_silent_timer(message: Message) -> None:
    try:
        argument = float(strings.get_command_argument(message.text)[0])
        config_handler.set_param('cacheTimeout', argument)
        await message.reply(f'Задержка начисления баллов в тихом режиме в минутах теперь <b>{argument}</b>')
    except Exception:
        await message.reply('<b>Введено неверное значение!</b>\n<i>Пример использования команды</i>\n/silenttimer 1.5')


@router.message(Command(commands=['setscore']), ChatType(chatType=['group', 'supergroup']), IsAdmin())
async def command_set_score(message: Message) -> None:
    try:
        argument = int(strings.get_command_argument(message.text)[0])
        config_handler.set_param('addedScoreAmount', argument)
        await message.reply(f'Количество начисляемых баллов теперь <b>{argument}</b>')
    except Exception:
        await message.reply('<b>Введено неверное значение!</b>\n<i>Пример использования команды</i>\n/setscore 2')


@router.message(Command(commands=['setscorename']), ChatType(chatType=['group', 'supergroup']), IsAdmin())
async def command_set_score_name(message: Message) -> None:
    try:
        arguments = strings.get_command_argument(message.text, 4, numeric=False)
        config_handler.set_score_names(arguments[0], arguments[1], arguments[2], arguments[3])
        await message.reply('<b>Название баллов изменено</b>')
    except Exception:
        await message.reply('<b>Введено неверное значение!</b>\n<i>Пример использования команды</i>\n/setscorename балл балла баллов баллы\n<i>(один)</i>  <i>(два)</i>  <i>(много)</i>  <i>(множественное число)</i>')


@router.message(Command(commands=['setregex']), ChatType(chatType=['group', 'supergroup']), IsAdmin())
async def command_set_regex(message: Message) -> None:
    try:
        argument = strings.get_command_argument(message.text, numeric=False)[0]
        config_handler.set_param('cacheTimeout', argument)
        await message.reply(f'Шаблон поиска теперь <b>{argument}</b>')
    except Exception:
        await message.reply('<b>Введено неверное значение!</b>\n<i>Пример использования команды</i>\n/setregex [Сс]пасибо|[Пп]ольза|[Пп]олезно|[Бб]лагодарю')


@router.message(Command(commands=['addscore']), ChatType(chatType=['group', 'supergroup']), IsAdmin())
async def add_score(message: Message) -> None:
    try:
        arguments = strings.get_command_argument(message.text, 2, numeric=False)
        targetId = arguments[0]
        addedScore = int(arguments[1])

        data_handler.add_user_score(userId=targetId, addedScore=addedScore)

    except:
        await message.reply('<b>Введено неверное значение!</b>\n<i>Пример использования команды</i>\n/addscore 050531206934 10')