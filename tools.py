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

def addScore(username:str, filePath:str) -> None:
    with open(filePath, 'r', encoding='utf8') as scoreFile:
        table = json.load(scoreFile)
        if username not in table:
            table[username] = 1
        else:
            table[username] += 1
    with open(filePath, 'w', encoding='utf8') as scoreFile:
        scoreFile.write(json.dumps(table))

def initList(filePath:str) -> None:
    with open(filePath, 'w', encoding='utf8') as scoreFile:
        scoreFile.write(json.dumps({}))

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
    initList(scoreListPath)
    with open('activeIn.json', 'w', encoding='utf8') as activeIds:
        activeIds.write(json.dumps([]))


if __name__ == '__main__':
    hardReset()