from aiogram import Router, F
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


@router.message(Command(commands=['givescore']),
                ChatType(chatType=['group', 'supergroup']),
                IsAdmin(),
                ~F.reply_to_message.from_user.is_bot,
                F.reply_to_message,
                F.reply_to_message.content_type != 'forum_topic_created'
                )
async def give_score(message: Message) -> None:
    try:
        arguments = strings.get_command_argument(message.text)
        targetUsername = message.reply_to_message.from_user.full_name
        targetUserId = message.reply_to_message.from_user.id
        givenScore = int(arguments[0])

        data_handler.add_user_score(username=targetUsername, userId=targetUserId, addedScore=givenScore)

        userScore = data_handler.get_user_score(targetUserId)
        replyTargetId = message.reply_to_message.message_id
        inlineMention = message.reply_to_message.from_user.mention_html()
        responseText = data_handler.get_response_text('scoreAdded').format(username = inlineMention, addedScore = givenScore,
                                                                           totalScore = userScore, scoreName = strings.get_score_name(givenScore))
        await message.answer(text=responseText, reply_to_message_id=replyTargetId, allow_sending_without_reply=True, disable_notification=True)

    except:
        await message.reply('<b>Введено неверное значение!</b>\n<i>Пример использования команды</i>\n/givescore 2\nКоманда должна быть отправлена в виде ответа на другое сообщение')


@router.message(Command(commands=['takescore']),
                ChatType(chatType=['group', 'supergroup']),
                IsAdmin(),
                ~F.reply_to_message.from_user.is_bot,
                F.reply_to_message,
                F.reply_to_message.content_type != 'forum_topic_created'
                )
async def take_score(message: Message) -> None:
    try:
        arguments = strings.get_command_argument(message.text)
        targetUsername = message.reply_to_message.from_user.full_name
        targetUserId = message.reply_to_message.from_user.id
        removedScore = int(arguments[0])

        data_handler.remove_user_score(username=targetUsername, userId=targetUserId, removedScore=removedScore)

        userScore = data_handler.get_user_score(targetUserId)
        replyTargetId = message.reply_to_message.message_id
        inlineMention = message.reply_to_message.from_user.mention_html()
        responseText = data_handler.get_response_text('scoreRemoved').format(username = inlineMention, removedScore = removedScore,
                                                                           totalScore = userScore, scoreName = strings.get_score_name(removedScore))
        await message.answer(text=responseText, reply_to_message_id=replyTargetId, allow_sending_without_reply=True, disable_notification=True)

    except ValueError:
        await message.reply('<b>Введено неверное значение!</b>\n<i>Пример использования команды</i>\n/takescore 2\nКоманда должна быть отправлена в виде ответа на другое сообщение')