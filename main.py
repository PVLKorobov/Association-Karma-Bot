from os.path import isfile
from telebot.async_telebot import AsyncTeleBot
from telebot import types
import asyncio
from configparser import ConfigParser
import set_commands
from tools import (logger, init_list, add_score, add_active, is_active, get_text_from_file, hard_reset, 
                   chat_reset, get_id_list, clear_score_cache, cache_save, str_to_dict, parse_cache, 
                   get_score_reply, get_score_name, get_named_score, parse_score_list)


def write_config(config:ConfigParser) -> None:
    with open('config.ini', 'w', encoding='utf8') as configFile:
        config.write(configFile)

def get_args(input:str) -> tuple|str:
    args = input.split()[1:]
    if len(args) == 1:
        return args[0]
    else:
        return tuple(args)
    
def check_files(scoreTablePath:str) -> None:
    activeListPath = './activeIn.json'

    if isfile(scoreTablePath) or isfile(activeListPath):
        log.info('Score table and active id list passed validation')
    else:
        log.warning('Score table or/and active id list are missing')
        hard_reset(scoreTablePath)
        log.warning('Score table and acive id list created')
    
async def check_commands(bot:AsyncTeleBot) -> None:
    log.info('Checking bot commands')
    if not config.getboolean('default', 'commandsinit'):
        log.warning('Bot commands are not set')
        await set_commands.set_private_scope(bot)
        await set_commands.set_admin_group_scope(bot)
        await set_commands.set_default_group_scope(bot)
        log.warning('Bot commands were set')

        config.set('default', 'commandsinit', 'True')
        write_config(config)
    else:
        log.info('Are set')

async def get_bot_name() -> str:
    user = await bot.get_me()
    return f'@{user.username}'

async def get_chat_title(chatId:int) -> str:
    chat = await bot.get_chat(chatId)
    return chat.title

async def is_admin(userId:int, chatId:int) -> bool:
    adminsList = await bot.get_chat_administrators(chatId)
    for admin in adminsList:
        if userId == admin.user.id:
            return True
    return False

async def print_cached(chatId:int) -> None:
    timer = config.getfloat("default", "cacheTime") * 60
    await asyncio.sleep(timer)
    log.info('Printing cached score data')
    config.set('default', 'cacheAwaits', 'False')
    write_config(config)
    scoreList = parse_cache(str(chatId), scoreNames)
    await bot.send_message(chatId, text=f'Начисленные недавно {scoreNames["low"]}ы\n{scoreList}')


if __name__ == '__main__':
    print('Бот запущен. Действия бота описаны в activity_log. Возникшие ошибки будут видны здесь')
    print('Чтобы отключить бота достаточно закрыть это окно')
    config = ConfigParser()
    config.read('config.ini', encoding='utf8')
    log = logger(config['default']['logFileLocation'])
    log.reset_log()
    bot = AsyncTeleBot(config['default']['accessToken'])
    log.info(f'Bot startup with config: {config.items("default")}')
    clear_score_cache()
    log.info('Cleaned score cache')
    config.set('default', 'cacheawaits', 'False')
    write_config(config)
    scoreNames = str_to_dict(config['default']['scoreNames'])

    asyncio.run(check_commands(bot))
    check_files(config['default']['scoreTableLocation'])


    @bot.message_handler(commands=['start'], chat_types=['supergroup', 'group'])
    async def start(message):
        if await is_admin(message.from_user.id, message.chat.id):
            log.info('/start group command run')
            if not is_active(message.chat.id):
                replyText = get_text_from_file('./responses/init.txt')
                add_active(message.chat.id)
                init_list(str(message.chat.id), config['default']['scoreTableLocation'])
                log.info(f'Bot work started in group {message.chat.title}')
                await bot.send_message(message.chat.id, replyText)
            else:
                replyText = get_text_from_file('./responses/failInit.txt')
                await bot.send_message(message.chat.id, replyText)
        else:
            await bot.reply_to(message, text='Извините, но вы не можете использовать эту команду')

    @bot.message_handler(commands=['start'], chat_types=['private'])
    async def start(message):
        log.info('/start private command run')
        with open('./responses/start.txt', 'r', encoding='utf8') as textFile:
            replyText = textFile.read()
            await bot.send_message(message.chat.id, replyText.format(name=message.from_user.username))

    @bot.message_handler(commands=['help'], chat_types=['supergroup', 'group'])
    async def help(message):
        log.info('/help group command run')
        if await is_admin(message.from_user.id, message.chat.id):
            replyText = get_text_from_file('./responses/adminHelp.txt')
        else:
            replyText = get_text_from_file('./responses/help.txt')
        await bot.reply_to(message, replyText)

    @bot.message_handler(commands=['help'], chat_types=['private'])
    async def help(message):
        log.info('/help private command run')
        replyText = get_text_from_file('./responses/helpPrivate.txt')
        await bot.send_message(message.chat.id, replyText)

    @bot.message_handler(commands=['reset'], chat_types=['supergroup', 'group'], func=lambda message: is_active(message.chat.id))
    async def reset(message):
        if await is_admin(message.from_user.id, message.chat.id):
            log.info('/reset command run')
            markup = types.InlineKeyboardMarkup()
            y = types.InlineKeyboardButton(text='Да', callback_data='y')
            n = types.InlineKeyboardButton(text='Нет', callback_data='n')
            markup.add(y, n)
            replyText = get_text_from_file('./responses/reset.txt')
            log.info(f'Created inline keyboard in message {message.id}')
            await bot.send_message(message.chat.id, replyText, reply_markup=markup)
        else:
            await bot.reply_to(message, text='Извините, но вы не можете использовать эту команду')
        
    @bot.callback_query_handler(func=lambda callback: callback.data == 'y' or callback.data == 'n')
    async def askReset(callback):
        await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=None)
        log.info(f'Removed inline keyboard of message {callback.message.id}')
        if callback.data == 'y':
            chat_reset(callback.message.chat.id, config['default']['scoreTableLocation'])
            log.warning(f'Bot soft reset in group {callback.message.chat.title}')
            replyText = 'Записи о полученных баллах очищены'
            await bot.send_message(callback.message.chat.id, replyText)

    @bot.message_handler(commands=['hardreset'], chat_types=['private'])
    async def HReset(message):
        if message.from_user.username == config['default']['allowedUser']:
            log.info('/hardreset command run')
            markup = types.InlineKeyboardMarkup()
            y = types.InlineKeyboardButton(text='Да', callback_data='yes')
            n = types.InlineKeyboardButton(text='Нет', callback_data='no')
            markup.add(y, n)
            replyText = get_text_from_file('./responses/hardReset.txt')
            log.info(f'Created inline keyboard in message {message.id}')
            await bot.send_message(message.chat.id, replyText, reply_markup=markup)
        else:
            await bot.reply_to(message, text='Извините, но вы не можете использовать эту команду')

    @bot.callback_query_handler(func=lambda callback: callback.data == 'yes' or callback.data == 'no')
    async def askHardReset(callback):
        await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=None)
        log.info(f'Removed inline keyboard of message {callback.message.id}')
        if callback.data == 'yes':
            log.warning('Bot hard reset initiated')
            idList = get_id_list()
            for chatId in idList:
                await bot.send_message(chatId, text='!Бот был перезапущен. Для начала работы в этом чате используйте команду /start')
            hard_reset(config['default']['scoreTableLocation'])
            replyText = 'Бот полностью перезапущен'
            log.warning('Bot hard reset complete')
            await bot.send_message(callback.message.chat.id, replyText)

    @bot.message_handler(commands=['silent'], func=lambda message: is_active(message.chat.id))
    async def toggleCaching(message):
        if await is_admin(message.from_user.id, message.chat.id):
            log.info('/silent command run')
            if config.getboolean('default', 'silentmode'):
                config.set('default', 'silentmode', 'False')
                write_config(config)
                log.info('Caching set to FALSE')
                await bot.send_message(message.chat.id, text='Начисления баллов будут записываться c оповещениями')
            else:
                config.set('default', 'silentmode', 'True')
                write_config(config)
                log.info('Caching set to TRUE')
                await bot.send_message(message.chat.id, text='Начисления баллов будут записываться без оповещений')
        else:
            await bot.reply_to(message, text='Извините, но вы не можете использовать эту команду')

    @bot.message_handler(commands=['silenttimer'], func=lambda message: is_active(message.chat.id))
    async def cacheTimeSet(message):
        if await is_admin(message.from_user.id, message.chat.id):
            log.info('/silenttimer command run')
            args = get_args(message.text)
            if type(args) is str and args != '' and float(args) > 0:
                config.set('default', 'cacheTime', args)
                write_config(config)
                log.info(f'cacheTime changed to {args}')
                await bot.reply_to(message, text=f'Задержка вывода данных теперь {args}')
            else:
                if len(args) == 0:
                    log.info(f'Blank /silenttimer arguments {args}')
                    await bot.reply_to(message, text='Использование команды /silenttimer\n/silenttimer [число минут]\nНапример: /silenttimer 1')
                else:
                    log.warning(f'Wrong /silenttimer arguments {args}')
                    await bot.reply_to(message, text='Введено неверное значение. Изменения не внесены')
        else:
            await bot.reply_to(message, text='Извините, но вы не можете использовать эту команду')

    @bot.message_handler(commands=['setscore'], chat_types=['group', 'supergroup'], func=lambda message: is_active(message.chat.id))
    async def setScore(message):
        if await is_admin(message.from_user.id, message.chat.id):
            log.info('/setscore command run')
            args = get_args(message.text)
            if type(args) is str and args != '' and int(args) > 0:
                config.set('default', 'addedscoreamount', args)
                write_config(config)
                log.info(f'AddedScoreAmount changed to {args}')
                await bot.reply_to(message, text=f'Количество начисляемых баллов теперь {args}')
            else:
                if len(args) == 0:
                    log.info(f'Blank /setscore arguments {args}')
                    await bot.reply_to(message, text='Использование команды /setscore\n/setscore [число]\nНапример: /setscore 8')
                else:
                    log.warning(f'Wrong /setscore arguments {args}')
                    await bot.reply_to(message, text='Введено неверное значение. Изменения не внесены')
        else:
            await bot.reply_to(message, text='Извините, но вы не можете использовать эту команду')

    # @bot.message_handler(commands=['scorenames'], chat_types=['group', 'supergroup'], func=lambda message: is_active(message.chat.id))
    # async def setScoreNames(message):
    #     if await is_admin(message.from_user.id, message.chat.id):
    #         log.info('/scorenames command run')
    #         args = getArgs(message.text)
    #         if type(args) is tuple and len(args) == 3:
    #             config.set('default', 'addedscoreamount', args)
    #             writeConfig(config)
    #             log.info(f'AddedScoreAmount changed to {args}')
    #             await bot.reply_to(message, text=f'Новые названия баллов - {args}')
    #         else:
    #             if len(args) == 0:
    #                 log.info(f'Blank /scorenames arguments {args}')
    #                 await bot.reply_to(message, text='Использование команды /scorenames\n/scorenames [1 балл] [2-4 балла] [более 5 баллов]\nНапример: /scorenames чек чека чеков')
    #             else:
    #                 log.warning(f'Wrong /scorenames arguments {args}')
    #                 await bot.reply_to(message, text='Введено неверное значение. Изменения не внесены')
    #     else:
    #         await bot.reply_to(message, text='Извините, но вы не можете использовать эту команду')

    @bot.message_handler(commands=['myscore'], chat_types=['group', 'supergroup'], func=lambda message: is_active(message.chat.id))
    async def myScore(message):
        log.info('/myscore command run')
        username = message.from_user.username
        score = get_named_score(username, str(message.chat.id), config['default']['scoreTableLocation'])
        if score != -1:
            scoreName = get_score_name(score, scoreNames)
            await bot.reply_to(message, text=f'@{username}  --  {score} {scoreName}')
        else:
            await bot.reply_to(message, text='Пока что вы не получили ни одного балла')


    @bot.message_handler(commands=['listscore'], chat_types=['group', 'supergroup'], func=lambda message: is_active(message.chat.id))
    async def listScore(message):
        log.info('/listscore command run')
        if await is_admin(message.from_user.id, message.chat.id):
            replyText = parse_score_list(str(message.chat.id), config['default']['scoreTableLocation'], scoreNames)
            if replyText == '':
                await bot.send_message(message.chat.id, text='В этой группе ещё не было начислено ни одного балла')
            else:
                await bot.send_message(message.chat.id, text=replyText)
        else:
            await bot.reply_to(message, text='Извините, но вы не можете использовать эту команду')


    @bot.message_handler(commands=['addscore'], chat_types=['group', 'supergroup'], func=lambda message: is_active(message.chat.id))
    async def manualScore(message):
        log.info('/addscore group command run')
        if await is_admin(message.from_user.id, message.chat.id):
            chatTitle = await get_chat_title(message.chat.id)
            replyText = get_text_from_file('./responses/addScoreFromGroup.txt')
            replyText = replyText.format(title=chatTitle, chatId=message.chat.id)
            await bot.send_message(message.from_user.id, text=replyText, parse_mode='MarkdownV2')
        else:
            await bot.reply_to(message, text='Извините, но вы не можете использовать эту команду')

    @bot.message_handler(commands=['addscore'], chat_types=['private'])
    async def handleScoreAdd(message):
        log.info('/addscore private command run')
        args = get_args(message.text)
        if type(args) is tuple and len(args) == 3 and int(args[2]) > 0:
            chatId = int(args[0])
            chatTitle = await get_chat_title(chatId)
            if is_active(chatId):
                if await is_admin(message.from_user.id, chatId):
                    if args[1][:1] == '@': username = args[1][1:]
                    else: username = args[1]
                    addedScore = int(args[2])
                    add_score(username, addedScore, str(chatId), config['default']['scoreTableLocation'])
                    log.info(f'{addedScore} score given to {username}')
                    scoreName = get_score_name(addedScore, scoreNames)
                    await bot.reply_to(message, text=f'{username} начислено {addedScore} {scoreName}')
                else:
                    await bot.reply_to(message, text=f'Извините, но вы не можете использовать эту команду, так как не являетесь администратором {chatTitle}')
            else:
                await bot.send_message(message.chat.id, text=f'Бот не активен в {chatTitle}. Добавьте бота в группу, если его там нет и используйте /start')
        else:
            if len(args) == 0:
                log.info(f'Blank /addscore arguments {args}')
                await bot.reply_to(message, text='Использование команды /addscore [id группы] [имя пользователя] [число баллов]\nНапример: /addscore -1362367688 @myUsername 15')
            else:
                log.warning(f'Wrong /addscore arguments {args}')
                await bot.reply_to(message, text='Введены неверные значения')

    @bot.message_handler(commands=['status'], chat_types=['supergroup', 'group'])
    async def getStatus(message):
        log.info('/status command run')
        if is_active(message.chat.id):
            replyText = get_text_from_file('./responses/status.txt')
            botName = await get_bot_name()
            chatTitle = await get_chat_title(message.chat.id)
            silentMode = '-'
            if config.getboolean('default', 'silentMode'):
                silentMode = 'Включен'
            else:
                silentMode = 'Отключен'
            silentTimer = config['default']['cacheTime']
            addedScore = config['default']['addedScoreAmount']
            replyText = replyText.format(botName=botName, chatName=chatTitle, silentStatus=silentMode, 
                                         silentTime=silentTimer, addedScoreAmount=addedScore,
                                         lowName=scoreNames['low'], midName=scoreNames['mid'], highName=scoreNames['high'])
            await bot.send_message(message.chat.id, text=replyText)
        else:
            await bot.send_message(message.chat.id, text='Бот неактивен в этом чате. Попробуйте команду /start')


    @bot.message_handler(regexp=config['default']['triggerRegex'], func=lambda message: message.reply_to_message != None and is_active(message.chat.id), chat_types=['supergroup', 'group'])
    async def messageReaction(message):
        addedScore = config.getint('default', 'addedScoreAmount')
        triggerName = message.from_user.username
        answerName = message.reply_to_message.from_user.username
        isBotAnswer = message.reply_to_message.from_user.is_bot
        log.info(f'Regex trigger on "{message.text}" from {triggerName} to {answerName}')
        if answerName != 'null' and triggerName != answerName and not isBotAnswer:
            if config.getboolean('default', 'silentMode'):
                add_score(answerName, addedScore, str(message.chat.id), config['default']['scoreTableLocation'])
                cache_save(answerName, addedScore, str(message.chat.id))
                if not config.getboolean('default', 'cacheawaits'):
                    config.set('default', 'cacheAwaits', 'True')
                    write_config(config)
                    await print_cached(message.chat.id)
                log.info(f"{addedScore} score given to {answerName} for {triggerName}'s approval")
            else:
                add_score(answerName, addedScore, str(message.chat.id), config['default']['scoreTableLocation'])
                log.info(f"{addedScore} score given to {answerName} for {triggerName}'s approval")
                replyLine = get_score_reply(answerName, int(addedScore), scoreNames)
                await bot.reply_to(message.reply_to_message, replyLine)


    asyncio.run(bot.polling())