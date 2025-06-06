import telebot
import os

# Получаем токен из переменных окружения
TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    raise ValueError("Переменная TELEGRAM_TOKEN не найдена. Укажите её в переменных окружения.")

# Создаем экземпляр бота
bot = telebot.TeleBot(TOKEN)

# Обработчик команд /start и /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот на Render. Задай мне вопрос!")

# Обработчик всех сообщений
@bot.message_handler(content_types=['text'])
def echo_all(message):
    bot.reply_to(message, f"Ты написал: {message.text}")

# Запуск бота с обработкой ошибок
try:
    bot.polling()
except Exception as e:
    print(f"Произошла ошибка: {e}")