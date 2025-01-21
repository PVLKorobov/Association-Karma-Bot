from typing import Any

import json

from os.path import isfile


#global
configPath = 'config.json'
#


def create_config_file(new: bool = True) -> None:
    if new:
        TOKEN = input("Введите токен бота >")
    else:
        TOKEN = config['accessToken']

    default_config = {'accessToken': TOKEN, 'triggerRegex': '[Сс]пасибо|[Пп]ольза|[Пп]олезно|[Бб]лагодарю', 'addedScoreAmount': 1, 'cacheTimeout': 0.5, 
                        'scoreNames': {'low': 'балл', 'mid': 'балла', 'high': 'баллов', 'plural': 'баллы'}}
    with open(configPath, 'w', encoding='utf8') as configFile:
        configFile.write(json.dumps(default_config, indent=4, ensure_ascii=False))


def read_config_file() -> dict:
    res = {}
    with open(configPath, 'r', encoding='utf8') as configFile:
        res = json.load(configFile)
    return res


def parse_config() -> dict:
    if not isfile('config.json'):
        create_config_file()
    return read_config_file()


#global
config = parse_config()
#


def write_config_file(data: dict) -> None:
    with open(configPath, 'w', encoding='utf8') as configFile:
        configFile.write(json.dumps(data, indent=4, ensure_ascii=False))


def set_param(paramName: str, paramValue: Any) -> None:
    config[paramName] = paramValue
    write_config_file(config)

def get_param(paramName: str) -> Any:
    return config[paramName]


def new_token():
    TOKEN = input("Введите новый токен бота >")
    set_param('accessToken', TOKEN)


def set_score_names(lowName: str, midName: str, highName: str, pluralName: str) -> None:
    scoreNames = get_param('scoreNames')
    scoreNames['low'] = lowName
    scoreNames['mid'] = midName
    scoreNames['high'] = highName
    scoreNames['plural'] = pluralName
    set_param('scoreNames', scoreNames)