import telebot
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from flask import Flask
from threading import Thread

# ========== КОНФИГУРАЦИЯ ==========
BOT_TOKEN = '8025037882:AAGg047cDKMWDF_w4pUh3H5qFfSBChJIkFo'
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

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
    "start": "👋 **Здравствуй, дорогой друг!**\n\nТы в TPHbot. Здесь уютно и полезно. Выбирай раздел! 👊",
    "energy": "📍 **⚡️ Энергия**\nБаза: 50. Таланты: +110. Сеты: Американец (+30), Дошик (+20).",
    "finka": "📍 **🗡 Финка**\nУрон: Кости (+225), Метки (+180), Ганнибал (+180).",
    "samopal": "📍 **🔫 Самопал**\nБонусы: Дюбель (+300), Миша (+210), Шайба (+160).",
    "poison": "📍 **🧪 Яд**\nНужен Талант Химик и Ашот 10 ур. Сет Чумной Доктор (+12%).",
    "bosses": "📍 **👊 Боссы**\nШайба (300к), Хирург (180м), Дюбель (240м), Гром (840м).",
    "sklad": "📍 **📦 Склад**\nРаздел в разработке. Скоро тут будет гайд по ресурсам!",
    "donate": "📍 **💎 Поддержка**\nСпасибо за твое доброе сердце! 🤝\nСвязь: @gbg_georg"
}

# ========== КНОПКИ ==========
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
    return InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Назад", callback_data="to_main"))

# ========== ОБРАБОТЧИКИ ==========
@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        bot.send_photo(message.chat.id, IMAGES["start"], caption=TEXTS["start"], reply_markup=kb_main(), parse_mode="Markdown")
    except:
        bot.send_message(message.chat.id, TEXTS["start"], reply_markup=kb_main(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    bot.answer_callback_query(call.id)
    cid, mid = call.message.chat.id, call.message.message_id
    
    def edit_ui(img_key, text, kb):
        try:
            bot.edit_message_media(InputMediaPhoto(IMAGES.get(img_key, IMAGES["start"]), caption=text, parse_mode="Markdown"), cid, mid, reply_markup=kb)
        except:
            try: bot.edit_message_caption(text, cid, mid, reply_markup=kb, parse_mode="Markdown")
            except: pass

    if call.data == "to_main": edit_ui("start", TEXTS["start"], kb_main())
    elif call.data == "m_energy": edit_ui("energy", TEXTS["energy"], kb_back())
    elif call.data == "m_finka": edit_ui("finka", TEXTS["finka"], kb_back())
    elif call.data == "m_samopal": edit_ui("samopal", TEXTS["samopal"], kb_back())
    elif call.data == "m_poison": edit_ui("poison", TEXTS["poison"], kb_back())
    elif call.data == "m_bosses": edit_ui("bosses", TEXTS["bosses"], kb_back())
    elif call.data == "m_sklad": edit_ui("sklad", TEXTS["sklad"], kb_back())
    elif call.data == "m_donate": edit_ui("donate", TEXTS["donate"], kb_back())
    elif call.data == "m_os": edit_ui("os", "💬 Пиши нам: @gbg_georg", kb_back())

# ========== ЗАПУСК ==========
@app.route('/')
def index(): return "Alive", 200

def run_bot():
    while True:
        try:
            bot.remove_webhook()
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"Ошибка: {e}")
            time.sleep(5)

if __name__ == "__main__":
    # Запускаем бота в отдельном потоке
    bot_thread = Thread(target=run_bot)
    bot_thread.start()
    # Flask запускается в основном потоке (так лучше для Render)
    app.run(host='0.0.0.0', port=8080)
