# 2.0 (02.08.2023)
<font size=4 style="color: teal">**В связи с переходом на фреймворк aiogram и изменением json структуры бота любые файлы предыдущих версий несовместимы с текущей!**</font>

## Что нового
### Для пользователей
- Перенесён функционал предыдущей версии в полном объёме.
- Упрощён процесс установки и первого запуска бота.
- Любые изменения настроек бота теперь происходят напрямую через чат с ботом.  
  Единственным исключением является получение и изменение токена доступа, требующее ввода напрямую в терминале бота. В первую очередь это связано с тем, что передача токена через чат нежелательна.
- Теперь бот свободно считает баллы пользователей всех чатов, в которые добавлен.

### С технической стороны
- Переход на фреймворк aiogram, и, соответственно, полная перепись кода бота.
- Новый код разбит на модули и пакеты для удобства дальнейшей разработки.
- Упрощение структуры json файлов бота.