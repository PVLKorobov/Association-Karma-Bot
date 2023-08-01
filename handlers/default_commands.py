from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from tools import config_handler, data_handler, strings
from tools.filters import ChatType


#global
router = Router()
#


@router.message(Command(commands=['help']), ChatType(chatType=['group', 'supergroup']))
async def command_help(message: Message) -> None:
    responseText = data_handler.get_response_text('help')
    await message.reply(responseText)


@router.message(Command(commands=['myscore']), ChatType(chatType=['group', 'supergroup']))
async def command_help(message: Message) -> None:
    userMention = message.from_user.mention_html()
    try:
        userScore = data_handler.get_user_score(message.from_user.id)
        responseText = data_handler.get_response_text('myScore').format(username=userMention, totalScore=userScore, scorename=strings.get_score_name(userScore))
    except Exception:
        responseText = data_handler.get_response_text('myScoreFail').format(username=userMention, scoreName=config_handler.get_param('scoreNames')['mid'])
    await message.reply(responseText)


@router.message(Command(commands=['start']), ChatType(chatType='private'))
async def command_start(message: Message) -> None:
    responseText = data_handler.get_response_text('start').format(username=message.from_user.mention_html)
    await message.reply(responseText)