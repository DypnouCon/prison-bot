import telebot
import time
import logging
import os
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from flask import Flask
from threading import Thread

# ========== НАСТРОЙКИ ==========
BOT_TOKEN = '8025037882:AAGg047cDKMWDF_w4pUh3H5qFfSBChJIkFo'
bot = telebot.TeleBot(BOT_TOKEN)

# Логирование в консоль Render
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ========== ВЕБ-СЕРВЕР ДЛЯ RENDER ==========
app = Flask('')

@app.route('/')
def home():
    return "I am alive"

def run_http():
    # Render сам назначит порт, мы его просто подхватываем
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_http)
    t.daemon = True # Позволяет потоку завершаться вместе с программой
    t.start()

# ========== ДАННЫЕ ГАЙДОВ ==========
GUIDES = {
    "⚡️ ЭНЕРГИЯ": "Гайд по энергии: Стандарт 50, Олимпиец +12, Лихой +20, Вой +15, Таланты: Адреналин +40.",
    "🗡 ФИНКА": "Гайд по финке: Кости +225, Пленник +180, Опасный +150, Ганнибал +180.",
    "🔫 САМОПАЛ": "Гайд по самопалу: Дьявольская удача +400, Русь +210, Совет +160.",
    "📞 ПОДДЕРЖКА": "Создатель: @gbg_georg"
}

def get_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*[KeyboardButton(name) for name in GUIDES.keys()])
    return markup

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "👋 Привет! Я готов к работе.", reply_markup=get_main_menu())

@bot.message_handler(func=lambda m: m.text in GUIDES)
def handle_guide(m):
    bot.send_message(m.chat.id, GUIDES[m.text], parse_mode='Markdown')

# ========== ЗАПУСК ==========
if __name__ == '__main__':
    print("--- ЗАПУСК СИСТЕМ ---")
    keep_alive() # Запуск Flask
    print("--- БОТ ПОШЕЛ В ПОЛЛИНГ ---")
    bot.polling(none_stop=True)
