import telebot
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from flask import Flask
from threading import Thread

# ========== НАСТРОЙКИ ==========
BOT_TOKEN = '8025037882:AAGg047cDKMWDF_w4pUh3H5qFfSBChJIkFo'
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask('')

START_IMG = "https://raw.githubusercontent.com/DypnouCon/prison-bot/main/starttext.jpeg"

# ========== ТЕКСТЫ ==========
TEXTS = {
    "start": (
        "🏠 **The Prison Helper**\n\n"
        "Информационная база знаний по игре. Собраны актуальные характеристики боссов, "
        "сетки урона и способы получения предметов.\n\n"
        "Выберите раздел для изучения:"
    ),
    
    "energy": (
        "📍 **Энергия**\n"
        "— — — — — — — — — —\n"
        "🔋 **Базовый запас:** 50 ед.\n\n"
        "🧬 **Таланты:**\n"
        "• Второе дыхание: +70 ед.\n"
        "• Адреналин: +40 ед.\n\n"
        "👕 **Одежда и комплекты:**\n"
        "• Американец (3 предмета из посылок): +30 ед.\n"
        "• Дошик (предмет из посылки): +20 ед.\n"
        "• Пирожок (Мастер Сева 7 ур.): +10 ед.\n"
        "• Четки (Мастер Ванька 10 ур.): +10 ед.\n\n"
        "📦 **Заныканный шмот и Сеты:**\n"
        "• Сет 'Робин Гуд' (все слоты у барыги): +39 ед.\n"
        "• Сет 'Лихие 90' (Слепой кольщик): +20 ед.\n"
        "• Сет 'Олимпиец': +12 ед."
    ),

    "finka_tats": (
        "📍 **Финка » Наколки**\n"
        "— — — — — — — — — —\n"
        "✍️ **Комплект 'Кости' (+225 урон)**\n"
        "• Тип: Сет из 12 наколок\n"
        "• Где: Тюрьма Кресты (Дневные/Ночные движухи)\n\n"
        "✍️ **Метки Судьбы (+180 урон)**\n"
        "• Тип: Сет из 34 наколок\n"
        "• Где: Комбо-бой с Авторитетным Шайбой\n\n"
        "✍️ **Комплект 'Пленник' (+180 урон)**\n"
        "• Тип: Сет из наколок\n"
        "• Где: Босс Пацанский Дядя Миша\n\n"
        "✍️ **Комплект 'Восток' (+160 урон)**\n"
        "• Где: Босс Пацанский Бурят\n\n"
        "✍️ **Принцесса (+80 урон)**\n"
        "• Где: Выигрыш в Катале"
    ),

    "finka_wear": (
        "📍 **Финка » Экипировка**\n"
        "— — — — — — — — — —\n"
        "👕 **Сет 'Ганнибал' (+180 урон)**\n"
        "• Тип: Комплект одежды\n"
        "• Где: Босс Авторитетный Хирург\n\n"
        "👕 **Сет 'Опасный' (+150 урон)**\n"
        "• Тип: Комплект одежды\n"
        "• Где: Босс Пацанский Хирург\n\n"
        "👕 **Сет 'Якудза' (+40 урон)**\n"
        "• Где: Босс Блатной Бурят\n\n"
        "👕 **Движухи (одежда):**\n"
        "• Армани (+35): Локация Угольки\n"
        "• К. Кляйн (+30): Локация Кресты\n"
        "• D&G (+25): Локация Лефортовка"
    ),

    "samopal": (
        "📍 **Самопал**\n"
        "— — — — — — — — — —\n"
        "🔫 **Базовый урон:** 70 ед.\n\n"
        "👊 **Боссы (предметы в сет):**\n"
        "• Дюбель (Авто): +300\n"
        "• Дядя Миша (Блат): +210\n"
        "• Шайба (Авто): +160\n\n"
        "🎰 **Азартные игры:**\n"
        "• Покер (Сет Дьявольская удача, 42 шт.): +400\n"
        "• Катала (Сет Падший Ангел, 34 шт.): +90\n"
        "• Колесо фортуны: +100\n\n"
        "🛠 **Мастера:**\n"
        "• Янка (Сет Обряд, 38 шт.): +80\n"
        "• Сет 'Тлен' (+90): бонус за всех мастеров"
    ),

    "bosses_bespredel": (
        "📍 **Боссы » Беспредельщики**\n"
        "— — — — — — — — — —\n"
        "🔘 **Шайба**\n"
        "Пац: 50к | Блат: 150к | Авто: 300к\n\n"
        "🔘 **Дядя Миша**\n"
        "Пац: 3м | Блат: 9м | Авто: 18м\n\n"
        "🔘 **Хирург**\n"
        "Пац: 30м | Блат: 90м | Авто: 180м\n\n"
        "🔘 **Тротил**\n"
        "Пац: 200м | Блат: 600м | Авто: 1.2б | Вор: 2.4б"
    ),

    "bosses_vertuhai": (
        "📍 **Боссы » Вертухаи**\n"
        "— — — — — — — — — —\n"
        "🔘 **Палыч:** 100 000\n"
        "🔘 **Близнецы:** 2 000 000\n"
        "🔘 **Борзов:** 3м / 9м / 18м\n"
        "🔘 **Дюбель:** 40м / 120м / 240м\n"
        "🔘 **Гром:** 70м / 210м / 420м / 840м"
    )
}

# ========== КНОПКИ ==========
def kb_main():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🔋 Энергия", callback_data="energy"),
        InlineKeyboardButton("🗡 Финка", callback_data="finka"),
        InlineKeyboardButton("🔫 Самопал", callback_data="samopal"),
        InlineKeyboardButton("👊 Боссы", callback_data="bosses"),
        InlineKeyboardButton("📦 Склад", callback_data="sklad"),
        InlineKeyboardButton("💎 Донат", callback_data="thanks")
    )
    kb.row(InlineKeyboardButton("💬 Обратная связь", url="https://t.me/gbg_georg"))
    return kb

def kb_finka():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("✍️ Наколки", callback_data="f_tats"),
        InlineKeyboardButton("👕 Экипировка", callback_data="f_wear"),
        InlineKeyboardButton("⬅️ Назад", callback_data="to_main")
    )
    return kb

def kb_bosses():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("💀 Беспредельщики", callback_data="b_bespredel"),
        InlineKeyboardButton("👮‍♂️ Вертухаи", callback_data="b_vertuhai"),
        InlineKeyboardButton("⬅️ Назад", callback_data="to_main")
    )
    return kb

# ========== ЛОГИКА ==========
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_photo(message.chat.id, START_IMG, caption=TEXTS["start"], reply_markup=kb_main(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    cid, mid = call.message.chat.id, call.message.message_id
    
    def edit(text, kb):
        try: bot.edit_message_caption(text, cid, mid, reply_markup=kb, parse_mode="Markdown")
        except: bot.send_message(cid, text, reply_markup=kb, parse_mode="Markdown")

    if call.data == "to_main": edit(TEXTS["start"], kb_main())
    elif call.data == "energy": edit(TEXTS["energy"], InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Назад", callback_data="to_main")))
    elif call.data == "finka": edit("📍 **Раздел: Финка**\nВыберите категорию:", kb_finka())
    elif call.data == "f_tats": edit(TEXTS["finka_tats"], InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Назад", callback_data="finka")))
    elif call.data == "f_wear": edit(TEXTS["finka_wear"], InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Назад", callback_data="finka")))
    elif call.data == "samopal": edit(TEXTS["samopal"], InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Назад", callback_data="to_main")))
    elif call.data == "bosses": edit("📍 **Раздел: Боссы**\nВыберите группировку:", kb_bosses())
    elif call.data == "b_bespredel": edit(TEXTS["bosses_bespredel"], InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Назад", callback_data="bosses")))
    elif call.data == "b_vertuhai": edit(TEXTS["bosses_vertuhai"], InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Назад", callback_data="bosses")))
    elif call.data == "sklad": edit("📦 **Склад**\n\nРаздел находится в разработке.", InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Назад", callback_data="to_main")))

# ========== ЗАПУСК ==========
@app.route('/')
def home(): return "OK"

if __name__ == '__main__':
    Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()
    bot.delete_webhook(drop_pending_updates=True)
    bot.polling(none_stop=True)
