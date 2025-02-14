from aiogram import Router, F
from aiogram.types import Message

from tools import config_handler, data_handler, strings
from tools.filters import ChatType, NotSelfReply


#global
router = Router()
#


@router.message(F.text.regexp(config_handler.get_param('triggerRegex')),
                ChatType(chatType=['group', 'supergroup']),
                ~F.reply_to_message.from_user.is_bot,
                F.reply_to_message,
                F.reply_to_message.content_type != 'forum_topic_created',
                NotSelfReply()
                )
async def trigger_message_handler(message: Message) -> None:
    username = message.reply_to_message.from_user.full_name
    userId = message.reply_to_message.from_user.id
    addedScore = config_handler.get_param('addedScoreAmount')
    data_handler.add_user_score(username=username, userId=userId, addedScore=addedScore)

    silentMode = data_handler.get_param('silentMode')
    cacheState = data_handler.get_param('cacheState')
    if silentMode:
        if not cacheState:
            data_handler.switch_cache_state()
            await data_handler.cache_timeout()
        data_handler.add_user_score(username, userId, addedScore, 'scoreCache')
        data_handler.add_chat_id(message.chat.id)
    else:
        userScore = data_handler.get_user_score(userId)
        replyTargetId = message.reply_to_message.message_id
        inlineMention = message.reply_to_message.from_user.mention_html()
        responseText = data_handler.get_response_text('scoreAdded').format(username = inlineMention, addedScore = addedScore,
                                                                           totalScore = userScore, scoreName = strings.get_score_name(addedScore))
        await message.answer(text=responseText, reply_to_message_id=replyTargetId, allow_sending_without_reply=True, disable_notification=True)