from datetime import datetime
import json


class logger:
    def __init__(self, logPath):
        self.log_filename = "activity_log.log"
        self.blank_entry = "[{time}][{type}]{message}\n"

# Очистка файла
    def reset_log(self):
        with open(self.log_filename, "w", encoding="utf-8") as log_file:
            log_file.write(f"[Bot started running at {self._get_current_time()}]\n")

# Получение времени в формате ЧЧ:ММ:СС
    def _get_current_time(self):
        now = datetime.now()
        return now.strftime("%H:%M:%S")

# Логирование состояния программы
    def info(self,message_input):
        entry = self.blank_entry
        current_time = self._get_current_time()
        with open(self.log_filename, "a", encoding="utf-8") as log_file:
            log_file.write(entry.format(time=current_time, type="INFO", message=message_input))

# Логирование предупреждения
    def warning(self, message_input):
        entry = self.blank_entry
        current_time = self._get_current_time()
        with open(self.log_filename, "a", encoding="utf-8") as log_file:
            log_file.write(entry.format(time=current_time, type="WARNING", message=message_input))

# Логирование ошибки
    def error(self, message_input):
        entry = self.blank_entry
        current_time = self._get_current_time()
        with open(self.log_filename, "a", encoding="utf-8") as log_file:
            log_file.write(entry.format(time=current_time, type="ERROR", message=message_input))
        print("Выполнение программы остановлено из-за ошибки. Информация об ошибке в activity_log")
        raise SystemExit(0)

def get_text_from_file(filePath:str) -> str:
    with open(filePath, 'r', encoding='utf8') as textFile:
        return textFile.read()

def add_score(username:str, scoreCount:int, chatId:str, scoreListPath:str) -> None:
    with open(scoreListPath, 'r', encoding='utf8') as scoreFile:
        table = json.load(scoreFile)
        if username not in table[chatId]:
            table[chatId][username] = scoreCount
        else:
            currentScore = int(table[chatId][username])
            table[chatId][username] = currentScore + scoreCount
    with open(scoreListPath, 'w', encoding='utf8') as scoreFile:
        scoreFile.write(json.dumps(table, indent=4))

def init_list(chatId:str, scoreListPath:str) -> None:
    with open(scoreListPath, 'r', encoding='utf8') as scoreFile:
        scoreDict = json.load(scoreFile)
        scoreDict[chatId] = {}
    with open(scoreListPath, 'w', encoding='utf8') as scoreFile:
        scoreFile.write(json.dumps(scoreDict, indent=4))

def add_active(chat_id:int) -> None:
    with open('activeIn.json', 'r', encoding='utf8') as activeIds:
        idList = json.load(activeIds)
        idList += [chat_id]
    with open('activeIn.json', 'w', encoding='utf8') as activeIds:
        activeIds.write(json.dumps(idList))

def is_active(chat_id:int) -> bool:
    with open('activeIn.json', 'r', encoding='utf8') as activeIds:
        return chat_id in json.load(activeIds)

def hard_reset(scoreListPath:str) -> None:
    with open(scoreListPath, 'w', encoding='utf8') as scoreFile:
        scoreFile.write(json.dumps({}))
    with open('activeIn.json', 'w', encoding='utf8') as activeIds:
        activeIds.write(json.dumps([]))

def get_id_list() -> list:
    with open('activeIn.json', 'r', encoding='utf8') as activeIds:
        return json.load(activeIds)
    
def chat_reset(chatId:int, scoreListPath:str) -> None:
    with open(scoreListPath, 'r', encoding='utf8') as scoreFile:
        table = json.load(scoreFile)
        table[str(chatId)] = {}
    with open(scoreListPath, 'w', encoding='utf8') as scoreFile:
        scoreFile.write(json.dumps(table, indent=4))

def str_to_dict(input:str) -> dict:
    return json.loads(input)

def cache_save(username:str, addedScore:int, chatId:str) -> None:
    with open('scoreCache.json', 'r', encoding='utf8') as scoreCache:
        cache = json.load(scoreCache)
        if chatId in cache:
            if username in cache[chatId]:
                currentScore = int(cache[chatId][username])
                cache[chatId][username] = currentScore + addedScore
            else:
                cache[chatId][username] = addedScore
        else:
            cache[chatId] = {username:addedScore}
    with open('scoreCache.json', 'w', encoding='utf8') as scoreCache:
        scoreCache.write(json.dumps(cache))

def clear_score_cache():
    with open('scoreCache.json', 'w', encoding='utf8') as scoreCache:
        scoreCache.write(json.dumps({}))

def get_score_name(score:int, scoreNames:dict) -> str:
    if (score > 1 and score < 5) or score == 0:
        return scoreNames['mid']
    if score > 4:
        return scoreNames['high']
    else:
        return scoreNames['low']

def parse_cache(chatId:str, scoreNames:dict) -> str:
    parsedLine = ''
    with open('scoreCache.json', 'r', encoding='utf8') as scoreCache:
        cache = json.load(scoreCache)
        for username in cache[chatId]:
            listedScore = cache[chatId][username]
            scoreName = get_score_name(listedScore, scoreNames)
            parsedLine += f'@{username} - {listedScore} {scoreName}\n'
    return parsedLine[:-1]

def get_score_reply(username:str, addedScore:int, scoreNames:dict) -> str:
    scoreName = get_score_name(addedScore, scoreNames)
    return f'@{username} получает {addedScore} {scoreName}'

def get_named_score(username:str, chatId:str, scoreListPath:str) -> int:
    with open(scoreListPath, 'r', encoding='utf8') as scoreTable:
        scores = json.load(scoreTable)
    if username in scores[chatId] and scores[chatId][username] > 0:
        return scores[chatId][username]
    else:
        return -1
    
def parse_score_list(chatId:str, scoreListPath:str, scoreNames:dict) -> str:
    with open(scoreListPath, 'r', encoding='utf8') as scoreTable:
        scores = json.load(scoreTable)
    res = ''
    for username in scores[chatId]:
        userScore = scores[chatId][username]
        scoreName = get_score_name(userScore, scoreNames)
        res += f'@{username}  --  {userScore} {scoreName}\n'
    return res[:-1]



if __name__ == '__main__':
    hard_reset('./scoreTable.json')