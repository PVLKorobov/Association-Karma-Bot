from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from tools import config_handler, data_handler, bot_commands, strings
from tools.filters import ChatType, IsAdmin
from tools.Bot import botInstance


#global
router = Router()
#


@router.message(Command(commands=['getauditlink']), ChatType(chatType=['group', 'supergroup']), IsAdmin())
async def get_audit_link_command(message: Message) -> None:
    responseText = "placeholder text"
    await message.reply(responseText)
    # TODO