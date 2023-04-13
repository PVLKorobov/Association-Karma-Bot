from telebot.async_telebot import AsyncTeleBot
from telebot import types
import asyncio
from configparser import ConfigParser
from tools import logger, initList, addScore, addActive, isActive, getTextFromFile, hardReset


if __name__ == '__main__':
    config = ConfigParser()
    config.read('config.ini', encoding='utf8')
    config = config['default']
    log = logger(config['logFileLocation'])
    log.reset_log()
    bot = AsyncTeleBot(config['accessToken'])
    bot.get_chat

    @bot.message_handler(commands=['start'], chat_types=['supergroup'])
    async def start(message):
        if not isActive(message.chat.id):
            replyText = getTextFromFile('./responses/init.txt')
            addActive(message.chat.id)
            await bot.send_message(message.chat.id, replyText)
        else:
            initList(config['scoreTableLocation'])
            replyText = getTextFromFile('./responses/failInit.txt')
            await bot.send_message(message.chat.id, replyText)

    @bot.message_handler(commands=['start'], chat_types=['private'])
    async def start(message):
        with open('./responses/start.txt', 'r', encoding='utf8') as textFile:
            replyText = textFile.read()
            await bot.send_message(message.chat.id, replyText.format(name=message.from_user.username))

    @bot.message_handler(commands=['help'], chat_types=['supergroup', 'private'])
    async def help(message):
        if message.chat.type == 'private':
            replyText = getTextFromFile('./responses/help.txt') + '\n/score - изменить количество баллов пользователя'
            await bot.send_message(message.chat.id, replyText)
        else:
            replyText = getTextFromFile('./responses/help.txt')
            await bot.send_message(message.chat.id, replyText)

    @bot.message_handler(commands=['reset'], chat_types=['supergroup', 'private'])
    async def reset(message):
        markup = types.InlineKeyboardMarkup()
        y = types.InlineKeyboardButton(text='Да', callback_data='y')
        n = types.InlineKeyboardButton(text='Нет', callback_data='n')
        markup.add(y, n)
        replyText = getTextFromFile('./responses/reset.txt')
        await bot.send_message(message.chat.id, replyText, reply_markup=markup)
        
    @bot.callback_query_handler(func=lambda callback: callback.data)
    async def yesNo(callback):
        if callback.data == 'y':
            hardReset(config['scoreTableLocation'])
            replyText = 'Бот перезапущен - вызовите команду /start'
            await bot.send_message(callback.message.chat.id, replyText)

    @bot.message_handler(regexp=config['triggerRegex'], func=lambda message: message.reply_to_message != None, chat_types=['supergroup'])
    async def messageReaction(message):
        addedScore = config['addedScoreAmount']
        triggerName = message.from_user.username
        answerName = message.reply_to_message.from_user.username
        isBotAnswer = message.reply_to_message.from_user.is_bot
        if triggerName != answerName and not isBotAnswer:
            addScore(answerName, config['scoreTableLocation'])
            log.info(f"{addedScore} score given to {answerName} for {triggerName}'s approval")
            await bot.reply_to(message.reply_to_message, f'@{answerName} получает {addedScore} (баллов)')

    asyncio.run(bot.polling())