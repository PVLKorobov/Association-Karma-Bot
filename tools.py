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

def getTextFromFile(filePath:str) -> str:
    with open(filePath, 'r', encoding='utf8') as textFile:
        return textFile.read()

def addScore(username:str, scoreCount:int, chatId:int, scoreListPath:str) -> None:
    with open(scoreListPath, 'r', encoding='utf8') as scoreFile:
        table = json.load(scoreFile)
        if username not in table:
            table[str(chatId)][username] = scoreCount
        else:
            table[str(chatId)][username] += scoreCount
    with open(scoreListPath, 'w', encoding='utf8') as scoreFile:
        scoreFile.write(json.dumps(table))

def initList(chatId:int, scoreListPath:str) -> None:
    with open(scoreListPath, 'r', encoding='utf8') as scoreFile:
        scoreDict = json.load(scoreFile)
        scoreDict[str(chatId)] = {}
    with open(scoreListPath, 'w', encoding='utf8') as scoreFile:
        scoreFile.write(json.dumps(scoreDict))

def addActive(chat_id:int) -> None:
    with open('activeIn.json', 'r', encoding='utf8') as activeIds:
        idList = json.load(activeIds)
        idList += [chat_id]
    with open('activeIn.json', 'w', encoding='utf8') as activeIds:
        activeIds.write(json.dumps(idList))

def isActive(chat_id:int) -> bool:
    with open('activeIn.json', 'r', encoding='utf8') as activeIds:
        return chat_id in json.load(activeIds)

def hardReset(scoreListPath:str) -> None:
    with open(scoreListPath, 'w', encoding='utf8') as scoreFile:
        scoreFile.write(json.dumps({}))
    with open('activeIn.json', 'w', encoding='utf8') as activeIds:
        activeIds.write(json.dumps([]))

def getIdList() -> list:
    with open('activeIn.json', 'r', encoding='utf8') as activeIds:
        return json.load(activeIds)
    
def chatReset(chatId:int, scoreListPath:str) -> None:
    with open(scoreListPath, 'r', encoding='utf8') as scoreFile:
        table = json.load(scoreFile)
        table[str(chatId)] = {}
    with open(scoreListPath, 'w', encoding='utf8') as scoreFile:
        scoreFile.write(json.dumps(table))

def strToDict(input:str) -> dict:
    return json.loads(input)

def cacheSave(username:str, addedScore:int, chatId:int) -> None:
    with open('scoreCache.json', 'w', encoding='utf8') as scoreCache:
        cache = json.load(scoreCache)
        if str(chatId) in cache:
            if username in cache[chatId]:
                cache[chatId][username] += addedScore
            else:
                cache[chatId][username] = addedScore
        else:
            cache[str(chatId)] = {username:addedScore}

def clearScoreCache():
    with open('scoreCache.json', 'w', encoding='utf8') as scoreCache:
        scoreCache.write(json.dumps({}))

def parseCache(chatId:int, scoreNames:dict) -> str:
    parsedLine = ''
    with open('scoreCache.json', 'r', encoding='utf8') as scoreCache:
        for username in scoreCache[str(chatId)]:
            scoreName = ''
            listedScore = scoreCache[str(chatId)][username]
            if (listedScore%10 > 1 and listedScore%10 < 5) or listedScore%10 == 0:
                scoreName = scoreNames['mid']
            if listedScore%10 > 4:
                scoreName = scoreNames['high']
            else:
                scoreName = scoreNames['low']
            parsedLine += f'{username} - {listedScore} {scoreName}\n'
    return parsedLine[:1]

def getScoreReply(username:str, addedScore:int, scoreNames:dict) -> str:
    scoreName = ''
    if (addedScore%10 > 1 and addedScore%10 < 5) or addedScore%10 == 0:
        scoreName = scoreNames['mid']
    if addedScore%10 > 4:
        scoreName = scoreNames['high']
    else:
        scoreName = scoreNames['low']
    return f'@{username} получает {addedScore} {scoreName}'



if __name__ == '__main__':
    hardReset('./scoreTable.json')