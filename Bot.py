import telebot
import os
import time  # <== добавлен импорт

print("Запуск бота...")

# Получаем токен из переменных окружения
TOKEN = os.getenv("7709844611:AAG1oI-9XUeMMvAClICiSNkntKfOclCV9ts")
if not TOKEN:
    print("Ошибка: TELEGRAM_TOKEN не найден. Проверь настройки переменных окружения в Render.")
    raise ValueError("Переменная TELEGRAM_TOKEN не найдена. Укажите её в переменных окружения.")

print("Токен успешно получен. Создаём бота...")

bot = telebot.TeleBot(TOKEN)

# Обработчик команд /start и /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    print(f"Получена команда: {message.text}")
    bot.reply_to(message, "Привет! Я бот на Render. Задай мне вопрос!")

# Обработчик всех текстовых сообщений
@bot.message_handler(content_types=['text'])
def echo_all(message):
    print(f"Получено сообщение: {message.text}")
    bot.reply_to(message, f"Ты написал: {message.text}")

# Запуск бота в бесконечном цикле
while True:
    try:
        print("Бот запущен! Ожидаю сообщения в Telegram...")
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print(f"Произошла ошибка: {e}. Переподключаюсь через 5 секунд...")
        time.sleep(5)