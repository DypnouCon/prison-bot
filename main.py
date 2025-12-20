import telebot
import os
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from flask import Flask
from threading import Thread

# ========== НАСТРОЙКИ ==========
BOT_TOKEN = '8025037882:AAGg047cDKMWDF_w4pUh3H5qFfSBChJIkFo'
bot = telebot.TeleBot(BOT_TOKEN)
server = Flask(__name__) # Изменил на server для ясности

BASE_URL = "https://raw.githubusercontent.com/DypnouCon/prison-bot/main/"
IMAGES = {
    "start": BASE_URL + "welcome.png",
    "energy": BASE_URL + "EnergyBloc.png",
    "finka": BASE_URL + "FinkaBloc.png",
    "samopal": BASE_URL + "SamopalBloc.png",
    "poison": BASE_URL + "PoiseBloc.png",
    "os": BASE_URL + "OSBloc.png",
    "donate": BASE_URL + "DonateBloc.png",
    "bosses": BASE_URL + "BossesBloc.png",
    "sklad": BASE_URL + "SkladBloc.png"
}

TEXTS = {
    "start": "🆕 **Prison Helper v1.6**\n\n👋 Привет! Если кнопки не работают, подожди 5 секунд и нажми /start еще раз. Бот просыпается! 👊",
    "energy": "📍 **Раздел: ⚡️ Энергия**\n— — — — — — — — — —\n🔋 База: 50 | Сеты: до +60 | Таланты: +110.",
    "finka": "📍 **Раздел: 🗡 Финка**\n— — — — — — — — — —\nТвой личный урон: наколки и шмот.",
    "samopal": "📍 **Раздел: 🔫 Самопал**\n— — — — — — — — — —\nУрон за сахар. Сеты боссов: Дюбель, Миша, Шайба.",
    "poison": "📍 **Раздел: 🧪 Яд**\n— — — — — — — — — —\nУрон флаконами. Качай Химика и Ашота!",
    "bosses": "📍 **Раздел: 👊 Боссы**\n— — — — — — — — — —\nВсе параметры авторитетов здесь.",
    "sklad": "📍 **Раздел: 📦 Склад**\n— — — — — — — — — —\nЛогистика ресурсов в разработке!",
    "donate": "📍 **Раздел: 💎 Донат**\n— — — — — — — — — —\nСпасибо за поддержку проекта! 🤝"
}

def kb_main():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("⚡️ Энергия", callback_data="m_energy"),
        InlineKeyboardButton("🗡 Финка", callback_data="m_finka"),
        InlineKeyboardButton("🔫 Самопал", callback_data="m_samopal"),
        InlineKeyboardButton("🧪 Яд", callback_data="m_poison"),
        InlineKeyboardButton("👊 Боссы", callback_data="m_bosses"),
        InlineKeyboardButton("📦 Склад", callback_data="m_sklad"),
        InlineKeyboardButton("💎 Донат", callback_data="m_donate")
    )
    kb.row(InlineKeyboardButton("💬 Обратная связь", callback_data="m_os"))
    return kb

def kb_back():
    return InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Назад в меню", callback_data="to_main"))

# ========== ОБРАБОТЧИКИ ==========
@bot.message_handler(commands=['start'])
def start(message):
    print(f">>> Команда /start от {message.chat.id}") # ЛОГ ДЛЯ ПРОВЕРКИ
    try:
        bot.send_photo(message.chat.id, IMAGES["start"], caption=TEXTS["start"], reply_markup=kb_main(), parse_mode="Markdown")
    except Exception as e:
        print(f"Ошибка START: {e}")
        bot.send_message(message.chat.id, TEXTS["start"], reply_markup=kb_main())

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    cid, mid = call.message.chat.id, call.message.message_id
    print(f">>> Клик: {call.data}") # ЛОГ ДЛЯ ПРОВЕРКИ
    
    def update_block(img_key, text, kb):
        try:
            new_media = InputMediaPhoto(IMAGES.get(img_key, IMAGES["start"]), caption=text, parse_mode="Markdown")
            bot.edit_message_media(new_media, cid, mid, reply_markup=kb)
        except Exception as e:
            print(f"UI Error: {e}")

    if call.data == "to_main": update_block("start", TEXTS["start"], kb_main())
    elif call.data == "m_energy": update_block("energy", TEXTS["energy"], kb_back())
    elif call.data == "m_finka": update_block("finka", TEXTS["finka"], kb_back())
    elif call.data == "m_samopal": update_block("samopal", TEXTS["samopal"], kb_back())
    elif call.data == "m_poison": update_block("poison", TEXTS["poison"], kb_back())
    elif call.data == "m_bosses": update_block("bosses", TEXTS["bosses"], kb_back())
    elif call.data == "m_sklad": update_block("sklad", TEXTS["sklad"], kb_back())
    elif call.data == "m_donate": update_block("donate", TEXTS["donate"], kb_back())
    elif call.data == "m_os": update_block("os", "💬 Связь: @gbg_georg", kb_back())

# ========== СЕРВЕР И ЗАПУСК ==========
@server.route('/')
def home():
    return "Bot is Alive", 200

def run_flask():
    server.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    # 1. Запускаем Flask в отдельном потоке
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()
    
    # 2. Очищаем старые сессии Telegram
    print("Очистка сессий...")
    bot.remove_webhook()
    bot.delete_webhook(drop_pending_updates=True)
    time.sleep(2)
    
    # 3. Запускаем бесконечный опрос
    print("Бот запущен!")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
