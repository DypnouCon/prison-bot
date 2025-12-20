import telebot
import os
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from flask import Flask
from threading import Thread

# ========== НАСТРОЙКИ ==========
BOT_TOKEN = '8025037882:AAGg047cDKMWDF_w4pUh3H5qFfSBChJIkFo'
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask('')

# Ссылки на GitHub (убедись, что названия файлов на хосте совпадают до буквы)
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

# ========== ТЕКСТЫ ==========
TEXTS = {
    "start": (
        "🆕 **Prison Helper v1.5**\n\n"
        "👋 Рады видеть тебя, дружище! Мы обновили визуальную составляющую бота.\n\n"
        "Выбирай нужный раздел ниже. Если меню пропало — введи /start 👊"
    ),
    "energy": (
        "📍 **Раздел: ⚡️ Энергия**\n"
        "— — — — — — — — — —\n"
        "🔋 База: 50 ед. | Таланты: +110 ед. (Второе дыхание + Адреналин)\n"
        "👕 Сеты: Американец (+30), Дошик (+20), Пирожок (+10)."
    ),
    "finka": (
        "📍 **Раздел: 🗡 Финка**\n"
        "— — — — — — — — — —\n"
        "Усиление личного урона через наколки и вещи.\n"
        "🦴 Кости: +225 | 👁 Метки: +180 | 👺 Ганнибал: +180"
    ),
    "samopal": (
        "📍 **Раздел: 🔫 Самопал**\n"
        "— — — — — — — — — —\n"
        "Оружие за сахар и рубли.\n"
        "👊 Макс. урон с сетов боссов: Дюбель (+300), Д.Миша (+210), Шайба (+160)."
    ),
    "poison": (
        "📍 **Раздел: 🧪 Яд**\n"
        "— — — — — — — — — —\n"
        "Независимый урон флаконами.\n"
        "🧪 Обязательно: Талант 'Химик' и Мастер Ашот 10 уровня."
    ),
    "bosses": (
        "📍 **Раздел: 👊 Боссы**\n"
        "— — — — — — — — — —\n"
        "💀 **Беспредельщики:** Шайба, Миша, Хирург, Тротил.\n"
        "👮‍♂️ **Вертухаи:** Палыч, Близнецы, Борзов, Дюбель, Гром."
    ),
    "sklad": (
        "📍 **Раздел: 📦 Склад**\n"
        "— — — — — — — — — —\n"
        "Здесь будет логистика ресурсов: сахар, мыло, бумага.\n"
        "🛠 Раздел наполняется на основе ваших отзывов!"
    ),
    "donate": (
        "📍 **Раздел: 💎 Донат**\n"
        "— — — — — — — — — —\n"
        "Дружище, бот работает на чистом энтузиазме.\n\n"
        "Твоя поддержка поможет нам оплачивать хостинг, чтобы бот летал 24/7. "
        "Любой вклад — это шаг к новым крутым разделам! 🤝"
    )
}

# ========== КЛАВИАТУРЫ ==========
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
    try:
        bot.send_photo(message.chat.id, IMAGES["start"], caption=TEXTS["start"], reply_markup=kb_main(), parse_mode="Markdown")
    except Exception as e:
        bot.send_message(message.chat.id, TEXTS["start"], reply_markup=kb_main(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    cid, mid = call.message.chat.id, call.message.message_id
    
    def update_block(img_key, text, kb):
        try:
            new_media = InputMediaPhoto(IMAGES.get(img_key, IMAGES["start"]), caption=text, parse_mode="Markdown")
            bot.edit_message_media(new_media, cid, mid, reply_markup=kb)
        except Exception as e:
            if "message is not modified" not in str(e):
                print(f"UI Error: {e}")

    # Навигация по меню
    if call.data == "to_main": update_block("start", TEXTS["start"], kb_main())
    elif call.data == "m_energy": update_block("energy", TEXTS["energy"], kb_back())
    elif call.data == "m_finka": update_block("finka", TEXTS["finka"], kb_back())
    elif call.data == "m_samopal": update_block("samopal", TEXTS["samopal"], kb_back())
    elif call.data == "m_poison": update_block("poison", TEXTS["poison"], kb_back())
    elif call.data == "m_bosses": update_block("bosses", TEXTS["bosses"], kb_back())
    elif call.data == "m_sklad": update_block("sklad", TEXTS["sklad"], kb_back())
    elif call.data == "m_donate": update_block("donate", TEXTS["donate"], kb_back())
    elif call.data == "m_os": update_block("os", "💬 Связь с разработчиком: @gbg_georg", kb_back())

# ========== ЗАПУСК ==========
@app.route('/')
def home(): return "OK"

def start_polling():
    try:
        bot.remove_webhook()
        bot.delete_webhook(drop_pending_updates=True)
        time.sleep(1) # Защита от Error 409
        print("Бот запущен и готов к фарму!")
        bot.polling(none_stop=True, skip_pending_updates=True)
    except Exception as e:
        print(f"Polling error: {e}")
        time.sleep(5)
        start_polling()

if __name__ == '__main__':
    Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()
    start_polling()
