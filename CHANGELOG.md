# 1.01 (26.04.2023)
- Теперь бот принимает команды от имени сообщества
**Команда /myscore недоступна от имени сообщества из-за необходимости id пользователя**
- Добавлена команда /setcommands. Вызов команды создаст меню команд, или перезапишет его, если оно уже существует
- Изменение структуры хранения начисленных баллов
    - Основным ключом теперь является id пользователя, а не username, чтобы избежать дубликатов в случае его отсутствия  
**В связи с изменениями временно отключена команда /addscore**  
- Исправлено накопление баллов в кэше "тихого" режима. Теперь он очищается после вывода
- Текст сообщения, отправляемого ботом при начислении баллов в обычном режиме вынесено в отдельный текстовый файл `scoreAdded.txt`, в директорию `responses`, и доступен для простого редактирования  
**Ознакомьтесь с приложенным файлом `!README.txt` перед редактированием файлов**

### Из-за изменения структуры хранения данных, для корректной работы бота необходима очистка сохранённых ранее данных

### В связи с отключением команды /addscore рекомендуется создать меню команд бота заново. *Данное действие не обязательно и не имеет эффекта на функционал бота*