import telebot
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice, ReplyKeyboardRemove
from flask import Flask
from threading import Thread

# ========== НАСТРОЙКИ ==========
BOT_TOKEN = '8025037882:AAGg047cDKMWDF_w4pUh3H5qFfSBChJIkFo'
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask('')

# ========== ТЕКСТЫ ГАЙДОВ ==========

TEXTS = {
    "start": (
        "📍 Главное меню\n\n"
        "The Prison Helper — ваш персональный справочник.\n\n"
        "Выберите раздел для детального изучения:"
    ),
    
    "energy": (
        "📍 Главное меню » Энергия\n\n"
        "Базовая энергия: 50\n\n"
        "Таланты:\n"
        "• Второе дыхание: +70\n"
        "• Адреналин: +40\n\n"
        "Одежда и мастера:\n"
        "• Американец (посылка): +30\n"
        "• Дошик (посылка): +20\n"
        "• Пирожок (Сева 7ур): +10\n"
        "• Четки (Ванька 10ур): +10\n"
        "• F1, Монетница, Радио: по +10\n\n"
        "Сеты и Заныканный шмот:\n"
        "• Робин Гуд (барыга): +39\n"
        "• Лихой (кольщик): +20\n"
        "• Вой (кольщик): +15\n"
        "• Олимпиец: +12"
    ),

    "finka_main": "📍 Главное меню » Финка\n\nВыберите категорию:",

    "finka_tats": (
        "📍 Главное меню » Финка » Наколки\n\n"
        "Кости: +225\n"
        "Кресты (день — верх, ночь — низ)\n\n"
        "Метки Судьбы: +180\n"
        "Комбо с Авто. Шайбой\n\n"
        "Пленник: +180\n"
        "Босс Пац. Дядя Миша\n\n"
        "Восток: +160\n"
        "Босс Пац. Бурят\n\n"
        "Принцесса: +80\n"
        "Выпадает в Катале\n\n"
        "Храм Мертвых: +70\n"
        "Комбо с Авто. Махно\n\n"
        "Мафиози / Зверинец: по +80"
    ),

    "finka_wear": (
        "📍 Главное меню » Финка » Шмотки\n\n"
        "Ганнибал: +180\n"
        "Босс Авто. Хирург\n\n"
        "Опасный: +150\n"
        "Босс Пац. Хирург\n\n"
        "Якудза: +40\n"
        "Босс Блат. Бурят\n\n"
        "Тюремные движухи:\n"
        "• Армани: +35 (Угольки)\n"
        "• К. Кляйн: +30 (Кресты)\n"
        "• D&G: +25 (Лефортовка)\n"
        "• Гучи / Гермес: +20\n\n"
        "Посылки (рука/тело):\n"
        "• Швейцарский ножик: +20\n"
        "• Майка: +30\n"
        "• Крюк: +10"
    ),

    "samopal": (
        "📍 Главное меню » Самопал\n\n"
        "Боссы:\n"
        "• Дюбель Авто: +300\n"
        "• Дядя Миша Блат: +210\n"
        "• Шайба Авто: +160\n"
        "• Близнецы: +150\n\n"
        "Мастера:\n"
        "• Янка (Обряд): +80\n"
        "• Паша Лесник: +30\n"
        "• Кеша (Толстосум): +40\n"
        "• Сет Тлен: +90 (Яша, Ашот, Жора, Сева, Шура, Илюша, Макар, Нинка)\n\n"
        "Азарт:\n"
        "• Покер (Дьявольская удача): +400\n"
        "• Катала (Падший Ангел): +90\n"
        "• Колесо фортуны: +100 (Жмурки + Знаток)"
    ),

    "bosses_main": "📍 Главное меню » Боссы\n\nВыберите категорию для просмотра ХП:",

    "bosses_bespredel": (
        "📍 Главное меню » Боссы » Беспредельщики\n\n"
        "Шайба:\n"
        "Пац: 50к | Блат: 150к | Авто: 300к\n\n"
        "Дядя Миша:\n"
        "Пац: 3м | Блат: 9м | Авто: 18м\n\n"
        "Хирург:\n"
        "Пац: 30м | Блат: 90м | Авто: 180м\n\n"
        "Тротил:\n"
        "Пац: 200м | Блат: 600м | Авто: 1.2б | Вор: 2.4б"
    ),

    "bosses_vertuhai": (
        "📍 Главное меню » Боссы » Вертухаи\n\n"
        "Палыч: 100к\n\n"
        "Близнецы: 2м\n\n"
        "Борзов:\n"
        "Пац: 3м | Блат: 9м | Авто: 18м\n\n"
        "Дюбель:\n"
        "Пац: 40м | Блат: 120м | Авто: 240м\n\n"
        "Гром:\n"
        "Пац: 70м | Блат: 210м | Авто: 420м | Вор: 840м"
    ),

    "thanks": (
        "📍 Главное меню » Благодарность\n\n"
        "Посылки с рублями (в игре):\n"
        "ID: 428871585\n\n"
        "Звезды Telegram:\n"
        "Кнопка оплаты ниже."
    )
}

# ========== КЛАВИАТУРЫ ==========

def kb_main():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("⚡️ Энергия", callback_data="energy"),
        InlineKeyboardButton("🗡 Финка", callback_data="finka"),
        InlineKeyboardButton("🔫 Самопал", callback_data="samopal"),
        InlineKeyboardButton("👊 Боссы", callback_data="bosses"),
        InlineKeyboardButton("💎 Благодарность", callback_data="thanks")
    )
    return kb

def kb_finka():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("✍️ Наколки", callback_data="f_tats"),
        InlineKeyboardButton("👕 Шмотки", callback_data="f_wear"),
        InlineKeyboardButton("⬅️ Назад", callback_data="back_main")
    )
    return kb

def kb_bosses():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("💀 Беспредельщики", callback_data="b_bespredel"),
        InlineKeyboardButton("👮‍♂️ Вертухаи", callback_data="b_vertuhai"),
        InlineKeyboardButton("⬅️ Назад", callback_data="back_main")
    )
    return kb

def kb_back(target):
    return InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Назад", callback_data=target))

# ========== ОБРАБОТЧИКИ ==========

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Загрузка...", reply_markup=ReplyKeyboardRemove())
    bot.send_message(message.chat.id, TEXTS["start"], reply_markup=kb_main())

@bot.callback_query_handler(func=lambda call: True)
def handle_call(call):
    data = call.data
    cid = call.message.chat.id
    mid = call.message.message_id

    if data == "back_main":
        bot.edit_message_text(TEXTS["start"], cid, mid, reply_markup=kb_main())
    
    elif data == "energy":
        bot.edit_message_text(TEXTS["energy"], cid, mid, reply_markup=kb_back("back_main"))
        
    elif data == "finka":
        bot.edit_message_text(TEXTS["finka_main"], cid, mid, reply_markup=kb_finka())
        
    elif data == "f_tats":
        bot.edit_message_text(TEXTS["finka_tats"], cid, mid, reply_markup=kb_back("finka"))
        
    elif data == "f_wear":
        bot.edit_message_text(TEXTS["finka_wear"], cid, mid, reply_markup=kb_back("finka"))
        
    elif data == "samopal":
        bot.edit_message_text(TEXTS["samopal"], cid, mid, reply_markup=kb_back("back_main"))

    elif data == "bosses":
        bot.edit_message_text(TEXTS["bosses_main"], cid, mid, reply_markup=kb_bosses())

    elif data == "b_bespredel":
        bot.edit_message_text(TEXTS["bosses_bespredel"], cid, mid, reply_markup=kb_back("bosses"))

    elif data == "b_vertuhai":
        bot.edit_message_text(TEXTS["bosses_vertuhai"], cid, mid, reply_markup=kb_back("bosses"))
        
    elif data == "thanks":
        kb = InlineKeyboardMarkup(row_width=1)
        kb.add(
            InlineKeyboardButton("✉️ Связь с автором", url="https://t.me/gbg_georg"),
            InlineKeyboardButton("⭐ Поддержать (50 Stars)", callback_data="pay"),
            InlineKeyboardButton("⬅️ Назад", callback_data="back_main")
        )
        bot.edit_message_text(TEXTS["thanks"], cid, mid, reply_markup=kb)

    elif data == "pay":
        bot.send_invoice(cid, "Донат", "Поддержка бота", "", "XTR", [LabeledPrice("Донат", 50)], "donate")

@bot.pre_checkout_query_handler(func=lambda q: True)
def checkout(q): bot.answer_pre_checkout_query(q.id, ok=True)

# ========== ЗАПУСК ==========

@app.route('/')
def home(): return "OK"

def run():
    bot.polling(none_stop=True)

if __name__ == '__main__':
    Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))).start()
    run()
