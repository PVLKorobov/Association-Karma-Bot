from telebot.async_telebot import AsyncTeleBot
from telebot import types
import asyncio
from configparser import ConfigParser
from tools import (logger, initList, addScore, addActive, isActive, getTextFromFile, hardReset, 
                   chatReset, getIdList, clearScoreCache, cacheSave, strToDict, parseCache, getScoreReply)


async def isAdmin(userId:int, chatId:int) -> bool:
    adminsList = await bot.get_chat_administrators(chatId)
    for admin in adminsList:
        if userId == admin.user.id:
            return True
    return False

async def printCached(chatId:int) -> None:
    timer = config.getint('default', 'cacheTime') * 60
    asyncio.sleep(timer)
    config.set('default', 'cacheStatus', 'False')
    scoreList = parseCache(chatId, scoreNames)
    await bot.send_message(chatId, text=f'Начисленные за последние {int(timer/60)} минут {scoreNames["low"]}ы\n{scoreList}')


if __name__ == '__main__':
    config = ConfigParser()
    config.read('config.ini', encoding='utf8')
    log = logger(config['default']['logFileLocation'])
    log.reset_log()
    bot = AsyncTeleBot(config['default']['accessToken'])
    log.info(f'Bot startup with config: {config.items("default")}')
    clearScoreCache()
    log.info('Cleaned score cache')
    config.set('default', 'cacheStatus', 'False')
    scoreNames = strToDict(config['default']['scoreNames'])


    @bot.message_handler(commands=['start'], chat_types=['supergroup', 'group'])
    async def start(message):
        if isAdmin(message.from_user.id, message.chat.id):
            if not isActive(message.chat.id):
                replyText = getTextFromFile('./responses/init.txt')
                addActive(message.chat.id)
                initList(message.chat.id, config['default']['scoreTableLocation'])
                await bot.send_message(message.chat.id, replyText)
            else:
                replyText = getTextFromFile('./responses/failInit.txt')
                await bot.send_message(message.chat.id, replyText)
        else:
            await bot.reply_to(message, text='Извините, но вы не можете использовать эту команду')

    @bot.message_handler(commands=['start'], chat_types=['private'])
    async def start(message):
        with open('./responses/start.txt', 'r', encoding='utf8') as textFile:
            replyText = textFile.read()
            await bot.send_message(message.chat.id, replyText.format(name=message.from_user.username))

    @bot.message_handler(commands=['help'], chat_types=['supergroup', 'group'])
    async def help(message):
        replyText = getTextFromFile('./responses/help.txt')
        await bot.send_message(message.chat.id, replyText)

    @bot.message_handler(commands=['help'], chat_types=['private'])
    async def help(message):
        replyText = getTextFromFile('./responses/helpPrivate.txt')
        await bot.send_message(message.chat.id, replyText)

    @bot.message_handler(commands=['reset'], chat_types=['supergroup', 'group'], func=lambda message: isActive(message.chat.id))
    async def reset(message):
        if isAdmin(message.from_user.id, message.chat.id):
            markup = types.InlineKeyboardMarkup()
            y = types.InlineKeyboardButton(text='Да', callback_data='y')
            n = types.InlineKeyboardButton(text='Нет', callback_data='n')
            markup.add(y, n)
            replyText = getTextFromFile('./responses/reset.txt')
            await bot.send_message(message.chat.id, replyText, reply_markup=markup)
        else:
            await bot.reply_to(message, text='Извините, но вы не можете использовать эту команду')
        
    @bot.callback_query_handler(func=lambda callback: callback.data == 'y' or callback.data == 'n')
    async def askReset(callback):
        await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=None)
        if callback.data == 'y':
            chatReset(callback.message.chat.id, config['default']['scoreTableLocation'])
            replyText = 'Записи о полученных баллах очищены'
            await bot.send_message(callback.message.chat.id, replyText)

    @bot.message_handler(commands=['hardreset'], chat_types=['private'])
    async def HReset(message):
        if message.from_user.username == config['default']['allowedUser']: # https://t.me/do_not_the_cat
            markup = types.InlineKeyboardMarkup()
            y = types.InlineKeyboardButton(text='Да', callback_data='yes')
            n = types.InlineKeyboardButton(text='Нет', callback_data='no')
            markup.add(y, n)
            replyText = getTextFromFile('./responses/hardReset.txt')
            await bot.send_message(message.chat.id, replyText, reply_markup=markup)
        else:
            await bot.reply_to(message, text='Извините, но вы не можете использовать эту команду')

    @bot.callback_query_handler(func=lambda callback: callback.data == 'yes' or callback.data == 'no')
    async def askHardReset(callback):
        await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=None)
        if callback.data == 'yes':
            idList = getIdList()
            for chatId in idList:
                await bot.send_message(chatId, text='[adminstag] Бот был перезапущен. Для начала работы в этом чате используйте команду /start')
            hardReset(config['default']['scoreTableLocation'])
            replyText = 'Бот полностью перезапущен'
            await bot.send_message(callback.message.chat.id, replyText)

    @bot.message_handler(commands=['cache'])

    @bot.message_handler(regexp=config['default']['triggerRegex'], func=lambda message: message.reply_to_message != None and isActive(message.chat.id), chat_types=['supergroup', 'group'])
    async def messageReaction(message):
        log.info(f'Regex trigger on {message.text}')
        addedScore = config['default']['addedScoreAmount']
        triggerName = message.from_user.username
        answerName = message.reply_to_message.from_user.username
        isBotAnswer = message.reply_to_message.from_user.is_bot
        if True:#triggerName != answerName and not isBotAnswer:
            if config.getboolean('default', 'silentMode'):
                addScore(answerName, addedScore, message.chat.id, config['default']['scoreTableLocation'])
                cacheSave(answerName, addedScore, message.chat.id)
                if config.getboolean('default', 'cacheStatus'):
                    printCached(message.chat.id)
                    config.set('default', 'cacheStatus', 'True')
                log.info(f"{addedScore} score given to {answerName} for {triggerName}'s approval")
            else:
                addScore(answerName, addedScore, message.chat.id, config['default']['scoreTableLocation'])
                log.info(f"{addedScore} score given to {answerName} for {triggerName}'s approval")
                replyLine = getScoreReply(answerName, addedScore, scoreNames)
                await bot.reply_to(message.reply_to_message, replyLine)


    asyncio.run(bot.polling())