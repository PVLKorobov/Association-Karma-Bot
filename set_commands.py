from telebot import TeleBot, types
from configparser import ConfigParser
from telebot.async_telebot import AsyncTeleBot


async def set_private_scope(bot:AsyncTeleBot):
    await bot.set_my_commands([
        types.BotCommand('/start', 'Start up the bot'),
        types.BotCommand('/help', 'List all available commands'),
    ], scope=types.BotCommandScopeAllPrivateChats())

async def set_admin_group_scope(bot:AsyncTeleBot):
    await bot.set_my_commands([
        types.BotCommand('/start', 'Start up the bot'),
        types.BotCommand('/help', 'List all available commands'),
        types.BotCommand('/myscore', 'See my score'),
        types.BotCommand('/listscore', 'List all user scores'),
        types.BotCommand('/reset', 'Reset bot in this chat'),
        types.BotCommand('/status', 'Check bot status'),
        types.BotCommand('/silent', 'Toggle silent mode'),
        types.BotCommand('/silenttimer', 'Set silent mode timer'),
        types.BotCommand('/setscore', 'Set added score amount'),
        types.BotCommand('/addscore', 'Manually add score to a user')
    ], scope=types.BotCommandScopeAllChatAdministrators())

async def set_default_group_scope(bot:AsyncTeleBot):
    await bot.set_my_commands([
        types.BotCommand('/myscore', 'See my score'),
        types.BotCommand('/help', 'List all available commands')
    ], scope=types.BotCommandScopeAllGroupChats())

# def set_trusted_user_scope(username):
#     bot.set_my_commands([
#         types.BotCommand('/start', 'Start up the bot'),
#         types.BotCommand('/help', 'List all available commands'),
#         types.BotCommand('/hardreset', '!!!Complete bot reset!!!')
#     ], scope=types.BotCommandScopeChat(f'@{username}'))


if __name__ == '__main__':
    config = ConfigParser()
    config.read('config.ini')
    bot = TeleBot(config['default']['accesstoken'])
    # trustedUsername = config['default']['allowedUser']

    set_private_scope()
    set_admin_group_scope()
    set_default_group_scope()
    # set_trusted_user_scope(trustedUsername)