from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message

from tools.Bot import botInstance


class ChatType(BaseFilter):
    def __init__(self, chatType: Union[str, list]) -> None:
        self.chatType = chatType

    async def __call__(self, message: Message) -> bool:
        if isinstance(self.chatType, str):
            return message.chat.type == self.chatType
        else:
            return message.chat.type in self.chatType
        

class NotSelfReply(BaseFilter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id != message.reply_to_message.from_user.id
    

class IsAdmin(BaseFilter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: Message) -> bool:
        adminList = await botInstance.get_chat_administrators(message.chat.id)
        for admin in adminList:
            if admin.user.id == message.from_user.id:
                return True
        return False