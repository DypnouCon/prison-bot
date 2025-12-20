import telebot
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from flask import Flask
from threading import Thread

# ========== КОНФИГУРАЦИЯ ==========
BOT_TOKEN = '8025037882:AAGg047cDKMWDF_w4pUh3H5qFfSBChJIkFo'
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# Прямые ссылки на RAW контент (обязательно проверяй наличие файлов на GitHub)
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
        "👋 **Здравствуй, дорогой друг!**\n\n"
        "Мы искренне рады видеть тебя в **TPHbot** (Prison Helper). "
        "Мир «Тюряги» суров, но с правильным напарником ты пройдешь через любые камеры. "
        "Выбирай интересующий раздел в меню ниже. Мы всегда рядом! 👊"
    ),
    "energy": (
        "📍 **⚡️ Энергия — твой главный ресурс**\n"
        "— — — — — — — — — —\n"
        "🧬 **Таланты (до +110 ед.):** Второе дыхание (+70), Адреналин (+40).\n"
        "👕 **Сеты:** Американец (+30), Дошик (+20), Пирожок (+10 - Сева 7 ур.).\n"
        "📿 **Мастерство:** Ванька (10 ур.) дает четки на +10 ед."
    ),
    "finka": (
        "📍 **🗡 Финка — твоя острая сила**\n"
        "— — — — — — — — — —\n"
        "✍️ **Наколки:** Сет «Кости» (+225 урон), Метки Судьбы (+180 урон).\n"
        "👺 **Экипировка:** Ганнибал (+180), Опасный (+150).\n"
        "Помни: наколки — это навсегда!"
    ),
    "samopal": (
        "📍 **🔫 Самопал — классика жанра**\n"
        "— — — — — — — — — —\n"
        "👊 **Боссы:** Дюбель (Авто) +300, Дядя Миша (Блат) +210, Шайба (Авто) +160.\n"
        "🛠 **Мастера:** Янка (+80) и сет «Тлен» (+90)."
    ),
    "poison": (
        "📍 **🧪 Яд — тихий убийца**\n"
        "— — — — — — — — — —\n"
        "🧪 **База:** Талант «Химик» и Мастер Ашот (10 ур.).\n"
        "👕 **Сеты:** Чумной Доктор (+12%), Лаборант (криты)."
    ),
    "bosses": (
        "📍 **👊 Боссы — проверка на прочность**\n"
        "— — — — — — — — — —\n"
        "💀 **Беспредельщики:** Шайба (300к), Миша (18м), Хирург (180м), Тротил (1.2б).\n"
        "👮‍♂️ **Вертухаи:** Палыч (100к), Борзов (18м), Дюбель (240м), Гром (840м)."
    ),
    "sklad": "📍 **📦 Склад**\n\nРаздел в наполнении. Готовим гайд по мылу и сахару! 🛠",
    "donate": (
        "📍 **💎 Поддержка проекта**\n"
        "— — — — — — — — — —\n"
        "Дорогой друг, наш бот живет благодаря твоей доброте.\n\n"
        "Твой вклад помогает нам оплачивать хостинг и делать новые гайды. "
        "Поддержать нас можно не только словом, но и делом:\n"
        "✨ **Звёзды Telegram**\n"
        "🎁 **Игровая валюта:** посылка «Рубли».\n\n"
        "Любая помощь бесценна. **Спасибо, что ты с нами!**"
    ),
    "os": (
        "📍 **💬 Обратная связь**\n"
        "— — — — — — — — — —\n"
        "Есть идеи или нашел ошибку? Пиши нашему разработчику, обсудим по-душам!\n\n"
        "Контакт: @gbg_georg"
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

def kb_back_donate():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("✨ Пожертвовать звёзды / Рубли", url="https://t.me/gbg_georg"))
    kb.add(InlineKeyboardButton("⬅️ Вернуться домой", callback_data="to_main"))
    return kb

def kb_back():
    return InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Вернуться домой", callback_data="to_main"))

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
            # Принудительное обновление медиа с новой картинкой
            new_photo = IMAGES.get(img_key, IMAGES["start"])
            bot.edit_message_media(
                InputMediaPhoto(new_photo, caption=text, parse_mode="Markdown"),
                cid, mid, reply_markup=kb
            )
        except Exception as e:
            print(f"Ошибка UI [{img_key}]: {e}")
            try: bot.edit_message_caption(text, cid, mid, reply_markup=kb, parse_mode="Markdown")
            except: pass

    # Навигация
    if call.data == "to_main": edit_ui("start", TEXTS["start"], kb_main())
    elif call.data == "m_energy": edit_ui("energy", TEXTS["energy"], kb_back())
    elif call.data == "m_finka": edit_ui("finka", TEXTS["finka"], kb_back())
    elif call.data == "m_samopal": edit_ui("samopal", TEXTS["samopal"], kb_back())
    elif call.data == "m_poison": edit_ui("poison", TEXTS["poison"], kb_back())
    elif call.data == "m_bosses": edit_ui("bosses", TEXTS["bosses"], kb_back())
    elif call.data == "m_sklad": edit_ui("sklad", TEXTS["sklad"], kb_back())
    elif call.data == "m_donate": edit_ui("donate", TEXTS["donate"], kb_back_donate())
    elif call.data == "m_os": edit_ui("os", TEXTS["os"], kb_back())

# ========== СЕРВЕР И ЗАПУСК ==========
@app.route('/')
def index(): return "TPHbot Online", 200

def run_bot():
    while True:
        try:
            bot.remove_webhook()
            bot.polling(none_stop=True, interval=1, timeout=60)
        except Exception as e:
            time.sleep(10)

if __name__ == "__main__":
    Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=8080)
