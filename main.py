import telebot
import os
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from flask import Flask
from threading import Thread

# ========== НАСТРОЙКИ ==========
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

# ========== ТЕКСТЫ ГАЙДОВ (ПОЛНЫЕ ВЕРСИИ) ==========
TEXTS = {
    "start": (
        "👋 **Рады видеть тебя в нашем кругу, дружище!**\n\n"
        "Ты зашел в Prison Helper — место, где мы по крупицам собираем всё, что поможет тебе "
        "стать авторитетнее и сильнее в мире «The Prison». Этот бот — твой верный напарник: "
        "подскажет, где выбить нужную наколку и как не слить ресурсы впустую.\n\n"
        "Чувствуй себя как дома. Осматривайся, изучай гайды. Удачного фарма! 👊"
    ),
    
    "energy": (
        "📍 **Главное меню » ⚡️ Энергия**\n"
        "— — — — — — — — — —\n"
        "🔋 **Базовый запас:** 50 ед.\n\n"
        "🧬 **Таланты (Максимум +110):**\n"
        "• Второе дыхание: +70 ед.\n"
        "• Адреналин: +40 ед.\n\n"
        "👕 **Комплекты одежды:**\n"
        "• Американец: +30 ед. (3 вещи)\n"
        "• Дошик: +20 ед.\n"
        "• Пирожок: +10 ед. (Мастер Сева 7 ур.)\n"
        "• Четки: +10 ед. (Мастер Ванька 10 ур.)\n\n"
        "🛠 **Совет:** Первым делом качай Севу до 7 уровня — это самый дешевый способ поднять лимит."
    ),

    "finka": (
        "📍 **Главное меню » 🗡 Финка**\n"
        "— — — — — — — — — —\n"
        "Усиление личного урона через наколки и вещи:\n\n"
        "✍️ **Топовые наколки:**\n"
        "• Комплект 'Кости': +225 урон (12 шт, локация Кресты)\n"
        "• Метки Судьбы: +180 урон (34 шт, Босс Авто-Шайба)\n\n"
        "👺 **Экипировка:**\n"
        "• Сет 'Ганнибал': +180 урон (Босс Авто-Хирург)\n"
        "• Сет 'Опасный': +150 урон (Босс Пац-Хирург)"
    ),

    "samopal": (
        "📍 **Главное меню » 🔫 Самопал**\n"
        "— — — — — — — — — —\n"
        "🔫 **Базовый урон:** 70 ед.\n\n"
        "👊 **Боссы (предметы в сет):**\n"
        "• Дюбель (Авто): +300\n"
        "• Дядя Миша (Блат): +210\n"
        "• Шайба (Авто): +160\n\n"
        "🛠 **Мастера:** Янка (+80), Сет 'Тлен' (+90)."
    ),

    "poison": (
        "📍 **Главное меню » 🧪 Яд**\n"
        "— — — — — — — — — —\n"
        "Независимый урон флаконами. Идеально для добивания.\n\n"
        "🧪 **Прокачка Химии:**\n"
        "• Талант 'Химик': Обязателен.\n"
        "• Мастер Ашот (10 ур.): Максимальный бонус к флаконам.\n\n"
        "👕 **Сеты:**\n"
        "• Чумной Доктор: +12% к урону.\n"
        "• Лаборант: Увеличивает шанс крита."
    ),

    "bosses": (
        "📍 **Главное меню » 👊 Боссы**\n"
        "— — — — — — — — — —\n"
        "💀 **Беспредельщики:**\n"
        "Шайба (300к) | Д.Миша (18м) | Хирург (180м) | Тротил (1.2б)\n\n"
        "👮‍♂️ **Вертухаи:**\n"
        "Палыч (100к) | Борзов (18м) | Дюбель (240м) | Гром (840м)"
    ),

    "sklad": "📦 **Склад**\n\nРаздел в доработке. Собираем ваши отзывы по трате сахара и мыла!",
    
    "donate": (
        "💎 **Поддержка проекта**\n"
        "— — — — — — — — — —\n"
        "Дружище, твой донат — это топливо для нашего бота.\n"
        "Все средства идут на оплату хостинга, чтобы Helper работал стабильно и быстро 24/7.\n\n"
        "Связь по всем вопросам: @gbg_georg"
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
    bot.send_photo(message.chat.id, IMAGES["start"], caption=TEXTS["start"], reply_markup=kb_main(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    cid, mid = call.message.chat.id, call.message.message_id
    
    # Убираем "часики" загрузки на кнопке сразу
    bot.answer_callback_query(call.id)
    
    def update_block(img_key, text, kb):
        try:
            new_media = InputMediaPhoto(IMAGES.get(img_key, IMAGES["start"]), caption=text, parse_mode="Markdown")
            bot.edit_message_media(new_media, cid, mid, reply_markup=kb)
        except Exception as e:
            if "message is not modified" not in str(e):
                print(f"UI Error: {e}")

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
@server.route('/')
def home(): return "OK", 200

def run_flask():
    server.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    Thread(target=run_flask).start()
    bot.remove_webhook()
    bot.delete_webhook(drop_pending_updates=True)
    time.sleep(1)
    print("Бот восстановлен и запущен!")
    bot.infinity_polling()
