from asyncio import sleep

from tools import config_handler
from tools.Bot import botInstance

from typing import Any
import json
from os.path import isfile


#global
dataPath = 'data.json'
#


# Structure:
"""
silentMode: bool
cacheState: bool
cacheChatIds: []
scoreCache: {
            userId: {username: str, score: int},
            ...
            }
listedUsers: {
            userId: {username: str, score: int},
            ...
            }
"""


def create_data_file() -> None:
    data = {'silentMode': False, 'cacheState': False, 'cacheChatIds': [], 'scoreCache': {}, 'listedUsers': {}}
    with open(dataPath, 'w', encoding='utf8') as dataFile:
        dataFile.write(json.dumps(data, indent=4, ensure_ascii=False, sort_keys=False))


def read_data_file() -> dict:
    with open(dataPath, 'r', encoding='utf8') as dataFile:
        res = json.load(dataFile)
    return res


def parse_data() -> dict:
    if not isfile(dataPath):
        create_data_file()
    return read_data_file()


#global
data = parse_data()
#


def text_file_response(fileName: str) -> str:
    responseText = None
    if isfile(f'responses/{fileName}'):
        with open(f'responses/{fileName}', 'r', encoding='utf8') as txtFile:
            responseText = txtFile.read()
    return responseText


def write_data_file(data: dict) -> None:
    with open(dataPath, 'w', encoding='utf8') as dataFile:
        dataFile.write(json.dumps(data, indent=4, ensure_ascii=False, sort_keys=False))


def add_user_score(userId: int, addedScore: int, tableName: str = 'listedUsers', username: str = '') -> None:
    userId = str(userId)
    if (not userId in data[tableName]) and (len(username) > 0):
        data[tableName][userId] = {'username': username, 'score': addedScore}
    else:
        data[tableName][userId]['score'] += addedScore
    write_data_file(data)


def remove_user_score(userId: int, removedScore: int, tableName: str = 'listedUsers', username: str = ''):
    userId = str(userId)
    if (not userId in data[tableName]) and (len(username) > 0):
        data[tableName][userId] = {'username': username, 'score': 0}
    else:
        if (data[tableName][userId]['score'] < removedScore):
            data[tableName][userId]['score'] = 0
        else:
            data[tableName][userId]['score'] -= removedScore
    write_data_file(data)


def get_user_score(userId: int) -> int:
    userId = str(userId)
    if userId in data['listedUsers']:
        res = data['listedUsers'][userId]['score']
        return res
    else:
        raise Exception


def get_response_text(responseName: str) -> str:
    with open(f'responses/{responseName}.txt', 'r', encoding='utf8') as textFile:
        res = textFile.read()
    return res


def get_score_table(tableName: str = 'listedUsers') -> str:
    res = ''
    for userId in data[tableName]:
        username = data[tableName][userId]['username']
        userScore = data[tableName][userId]['score']

        res += f'<a href="tg://user?id={userId}">{username}</a>  ---  <b>{userScore}</b>\n'
    return res[:-1]


def get_param(paramName: str) -> Any:
    return data[paramName]


def set_param(paramName: str, paramValue: Any) -> None:
    data[paramName] = paramValue
    write_data_file(data)


def switch_cache_state():
    set_param('cacheState', not get_param('cacheState'))


def add_chat_id(chatId: int):
    chatId = str(chatId)
    if chatId not in data['cacheChatIds']:
        data['cacheChatIds'].append(chatId)
        write_data_file(data)


def clear_cache():
    cachedChatIds = get_param('cacheChatIds')
    cache = get_param('scoreCache')
    if len(cachedChatIds) != 0:
        data['cacheChatIds'] = []
    if len(cache) != 0:
        data['scoreCache'] = {}
    
    write_data_file(data)


#global
clear_cache()
#


async def cache_timeout():
    timeoutMinutes = config_handler.get_param('cacheTimeout')
    await sleep(timeoutMinutes * 60)
    
    switch_cache_state()
    cacheScoreTable = get_score_table('scoreCache')
    chatIds = data['cacheChatIds']

    responseText = get_response_text('scoreCache').format(scoreName=config_handler.get_param('scoreNames')['plural'], scoreTable=cacheScoreTable)
    for chatId in chatIds:
        await botInstance.send_message(text=responseText, chat_id=chatId, disable_notification=True)
    
    clear_cache()