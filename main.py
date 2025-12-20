import telebot
import os
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from flask import Flask
from threading import Thread

# ========== КОНФИГУРАЦИЯ ==========
BOT_TOKEN = '8025037882:AAGg047cDKMWDF_w4pUh3H5qFfSBChJIkFo'
bot = telebot.TeleBot(BOT_TOKEN)
server = Flask(__name__)

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

# ========== ТЕКСТЫ (МАКСИМАЛЬНОЕ НАПОЛНЕНИЕ) ==========
TEXTS = {
    "start": (
        "👋 **Здравствуй, дорогой друг!**\n\n"
        "Мы искренне рады видеть тебя в **TPHbot** (Prison Helper). Ты попал в уютный уголок, "
        "созданный игроками для игроков. Здесь нет суеты, только полезные знания.\n\n"
        "Выбирай интересующий раздел в меню ниже. Мы всегда рядом! 👊"
    ),
    "energy": (
        "📍 **⚡️ Энергия — твой главный ресурс**\n"
        "— — — — — — — — — —\n"
        "🔋 **Базовый запас:** 50 ед.\n\n"
        "🧬 **Таланты (до +110 ед.):**\n"
        "• *Второе дыхание:* +70 к лимиту.\n"
        "• *Адреналин:* +40 к лимиту.\n\n"
        "👕 **Сеты одежды:**\n"
        "• **Американец:** +30 ед. (штаны, куртка, ботинки).\n"
        "• **Дошик:** +20 ед.\n"
        "• **Пирожок:** +10 ед. (Сева 7 ур.).\n\n"
        "📿 **Мастерство:**\n"
        "Ванька (10 ур.) дает четки на +10 ед. энергии.\n\n"
        "*Совет: Сначала качай таланты, это база!*"
    ),
    "finka": (
        "📍 **🗡 Финка — твоя личная мощь**\n"
        "— — — — — — — — — —\n"
        "✍️ **Наколки:**\n"
        "• **Кости:** +225 урон (12 шт., Кресты).\n"
        "• **Метки Судьбы:** +180 урон (34 шт., Авто-Шайба).\n\n"
        "👺 **Экипировка:**\n"
        "• **Ганнибал:** +180 урон (Авто-Хирург).\n"
        "• **Опасный:** +150 урон (Пац-Хирург).\n\n"
        "*Наколки — твой вечный капитал. Начинай с Костей!*"
    ),
    "samopal": (
        "📍 **🔫 Самопал — классика**\n"
        "— — — — — — — — — —\n"
        "👊 **Бонусы от сетов:**\n"
        "• **Дюбель (Авто):** +300 к урону.\n"
        "• **Дядя Миша (Блат):** +210 к урону.\n"
        "• **Шайба (Авто):** +160 к урону.\n\n"
        "🛠 **Мастера:**\n"
        "Янка (+80) и сет «Тлен» (+90).\n\n"
        "*Самопал бьет редко, но метко. Не жалей сахара!*"
    ),
    "poison": (
        "📍 **🧪 Яд — смертельный коктейль**\n"
        "— — — — — — — — — —\n"
        "🧪 **База:**\n"
        "Талант «Химик» и Мастер Ашот (10 ур.) — без них яд не работает.\n\n"
        "👕 **Сеты:**\n"
        "• **Чумной Доктор:** +12% к урону флаконами.\n"
        "• **Лаборант:** увеличивает шанс крита.\n\n"
        "*Используй яд на боссах с большим HP!*"
    ),
    "bosses": (
        "📍 **👊 Боссы зоны**\n"
        "— — — — — — — — — —\n"
        "💀 **Беспредельщики:**\n"
        "• Шайба: 300к | Миша: 18м | Хирург: 180м | Тротил: 1.2б\n\n"
        "👮‍♂️ **Вертухаи:**\n"
        "• Палыч: 100к | Борзов: 18м | Дюбель: 240м | Гром: 840м\n\n"
        "*Для каждого босса нужна своя тактика и время!*"
    ),
    "sklad": (
        "📍 **📦 Склад и ресурсы**\n"
        "— — — — — — — — — —\n"
        "Тут скоро будет гайд по трате мыла, сахара и бумаги.\n"
        "Мы готовим для тебя лучшие схемы обмена! 🛠"
    ),
    "donate": (
        "📍 **💎 Поддержка**\n"
        "— — — — — — — — — —\n"
        "Любой вклад помогает нам оплачивать хостинг.\n"
        "Спасибо за твое доброе сердце! 🤝\n"
        "Связь: @gbg_georg"
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
    return InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Назад", callback_data="to_main"))

# ========== ОБРАБОТЧИКИ ==========
@bot.message_handler(commands=['start'])
def start(message):
    try:
        bot.send_photo(message.chat.id, IMAGES["start"], caption=TEXTS["start"], reply_markup=kb_main(), parse_mode="Markdown")
    except:
        bot.send_message(message.chat.id, TEXTS["start"], reply_markup=kb_main(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    cid, mid = call.message.chat.id, call.message.message_id
    bot.answer_callback_query(call.id) # Мгновенно убирает загрузку
    
    def update_ui(img_key, text, kb):
        try:
            media = InputMediaPhoto(IMAGES.get(img_key, IMAGES["start"]), caption=text, parse_mode="Markdown")
            bot.edit_message_media(media, cid, mid, reply_markup=kb)
        except Exception as e:
            try: bot.edit_message_caption(text, cid, mid, reply_markup=kb, parse_mode="Markdown")
            except: pass

    if call.data == "to_main": update_ui("start", TEXTS["start"], kb_main())
    elif call.data == "m_energy": update_ui("energy", TEXTS["energy"], kb_back())
    elif call.data == "m_finka": update_ui("finka", TEXTS["finka"], kb_back())
    elif call.data == "m_samopal": update_ui("samopal", TEXTS["samopal"], kb_back())
    elif call.data == "m_poison": update_ui("poison", TEXTS["poison"], kb_back())
    elif call.data == "m_bosses": update_ui("bosses", TEXTS["bosses"], kb_back())
    elif call.data == "m_sklad": update_ui("sklad", TEXTS["sklad"], kb_back())
    elif call.data == "m_donate": update_ui("donate", TEXTS["donate"], kb_back())
    elif call.data == "m_os": update_ui("os", "💬 Пиши нам: @gbg_georg", kb_back())

# ========== ЗАПУСК ==========
@server.route('/')
def home(): return "OK", 200

def run_flask():
    server.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    Thread(target=run_flask).start()
    
    # Жесткий сброс для предотвращения 409
    try:
        bot.stop_polling()
        time.sleep(3)
        bot.remove_webhook()
        bot.delete_webhook(drop_pending_updates=True)
    except:
        pass
        
    print("Бот проснулся!")
    bot.infinity_polling(skip_pending_updates=True)
