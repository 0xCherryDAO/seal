## Для использования

Для установки библиотеки pysui необходимо <a href="https://www.rust-lang.org/tools/install">скачать</a> Rust

Версия python - 3.11 и выше

## Конфиг
В папку images загружаем картинки в формате ['.jpg', '.jpeg', '.png', '.bmp', '.webp']

### Опциональные настройки:

`CAPSOLVER_API` — API для решения капчи крана (https://dashboard.capsolver.com/)

`TG_BOT_TOKEN` — токен телеграм бота для уведомлений. Можно оставить `TG_BOT_TOKEN = None`. Создать тут - @BotFather

`TG_USER_ID` — цифровой айди пользователя, куда будут приходить уведомления. Можно узнать тут - @userinfobot

### Настройки:
`FAUCET`— Получение токенов с крана

`UPLOAD_FILE`— Загрузка файлов в seal

`number_of_uploads`— Количество загрузок

`create_new_entry`— Создавать ли новые entry или грузить в один

## Установка и запуск
```bash
pip install -r requirements.txt

# Перед запуском необходимо настроить модули в config.py
python main.py
```