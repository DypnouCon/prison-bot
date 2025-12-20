import telebot
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice
from flask import Flask
from threading import Thread

# ========== НАСТРОЙКИ ==========
BOT_TOKEN = '8025037882:AAGg047cDKMWDF_w4pUh3H5qFfSBChJIkFo'
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask('')

# Функция для получения прямой ссылки GitHub
def get_raw(url):
    return url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")

# Ссылки на картинки
IMG = {
    "main": get_raw("https://github.com/DypnouCon/prison-bot/blob/main/persten.png"),
    "energy": get_raw("https://github.com/DypnouCon/prison-bot/blob/main/hidesicon.png"),
    "finka": get_raw("https://github.com/DypnouCon/prison-bot/blob/main/knife.png"),
    "samopal": get_raw("https://github.com/DypnouCon/prison-bot/blob/main/gunIcon.png"),
    "bosses": get_raw("https://github.com/DypnouCon/prison-bot/blob/main/Avtoritet.png"),
    "sklad": get_raw("https://github.com/DypnouCon/prison-bot/blob/main/sugar.png")
}

# ========== ТЕКСТЫ ГАЙДОВ ==========
TEXTS = {
    "start": (
        "🏠 **Добро пожаловать в Prison Helper!**\n\n"
        "Этот бот создан для помощи в игре «The Prison». Здесь собрана и постоянно дополняется "
        "вся важная информация для облегчения поиска знаний об игровых механиках.\n\n"
        "Выберите интересующий раздел ниже:"
    ),
    "sklad": "📦 **Склад**\n\nУпс... ты застал меня врасплох за активной работой. Скоро этот раздел будет заполнен рекомендациями!",
    "energy": (
        "📍 Энергия\n\n"
        "База: 50. Таланты: Второе дыхание (+70), Адреналин (+40).\n\n"
        "Одежда: Американец (+30), Дошик (+20), Пирожок (+10, Сева 7ур), Четки (+10, Ванька 10ур).\n\n"
        "Заныканный шмот: Робин Гуд (+39), Лихие 90 (+20), Олимпиец (+12)."
    ),
    "finka_main": "📍 Финка\n\nВыберите категорию для прокачки урона:",
    "finka_tats": "📍 Финка » Наколки\n\nКости (+225): Кресты.\nМетки Судьбы (+180): Комбо Шайба.\nПленник (+180): Дядя Миша.\nЗверинец (+80): Магазин.",
    "finka_wear": "📍 Финка » Шмотки\n\nГаннибал (+180): Хирург Авто.\nОпасный (+150): Хирург Пац.\nЯкудза (+40): Бурят Блат.\nАрмани (+35): Угольки.",
    "samopal": (
        "📍 Самопал\n\n"
        "Боссы: Дюбель (+300), Д.Миша (+210), Шайба (+160).\n"
        "Азарт: Покер (+400), Катала (+90), Колесо (+50).\n"
        "Мастера: Янка (+80), Кеша (+40), Сет Тлен (+90)."
    ),
    "bosses_bespredel": (
        "📍 Боссы » Беспредельщики\n\n"
        "Шайба: 50к / 150к / 300к\n"
        "Дядя Миша: 3м / 9м / 18м\n"
        "Хирург: 30м / 90м / 180м\n"
        "Тротил: 200м / 600м / 1.2б / 2.4б"
    ),
    "bosses_vertuhai": (
        "📍 Боссы » Вертухаи\n\n"
        "Палыч: 100к\n"
        "Близнецы: 2м\n"
        "Борзов: 3м / 9м / 18м\n"
        "Дюбель: 40м / 120м / 240м\n"
        "Гром: 70м / 210м / 420м / 840м"
    )
}

# ========== КЛАВИАТУРЫ ==========
def get_main_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("⚡️ Энергия", callback_data="energy"),
        InlineKeyboardButton("🗡 Финка", callback_data="finka"),
        InlineKeyboardButton("🔫 Самопал", callback_data="samopal"),
        InlineKeyboardButton("👊 Боссы", callback_data="bosses"),
        InlineKeyboardButton("📦 Склад", callback_data="sklad"),
        InlineKeyboardButton("💎 Донат", callback_data="thanks")
    )
    kb.row(InlineKeyboardButton("💬 Обратная связь", url="https://t.me/gbg_georg"))
    return kb

def get_bosses_kb():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("💀 Беспредельщики", callback_data="b_bespredel"),
        InlineKeyboardButton("👮‍♂️ Вертухаи", callback_data="b_vertuhai"),
        InlineKeyboardButton("⬅️ Назад", callback_data="to_main")
    )
    return kb

def get_back_kb(target):
    return InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Назад", callback_data=target))

# ========== ОБРАБОТЧИКИ ==========
def send_update(call, text, img_key, keyboard):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_photo(call.message.chat.id, IMG[img_key], caption=text, reply_markup=keyboard, parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_photo(message.chat.id, IMG["main"], caption=TEXTS["start"], reply_markup=get_main_kb(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "to_main":
        send_update(call, TEXTS["start"], "main", get_main_kb())
    elif call.data == "energy":
        send_update(call, TEXTS["energy"], "energy", get_back_kb("to_main"))
    elif call.data == "finka":
        send_update(call, TEXTS["finka_main"], "finka", InlineKeyboardMarkup().add(
            InlineKeyboardButton("✍️ Наколки", callback_data="f_tats"),
            InlineKeyboardButton("👕 Шмотки", callback_data="f_wear"),
            InlineKeyboardButton("⬅️ Назад", callback_data="to_main")
        ))
    elif call.data == "f_tats":
        send_update(call, TEXTS["finka_tats"], "finka", get_back_kb("finka"))
    elif call.data == "f_wear":
        send_update(call, TEXTS["finka_wear"], "finka", get_back_kb("finka"))
    elif call.data == "samopal":
        send_update(call, TEXTS["samopal"], "samopal", get_back_kb("to_main"))
    elif call.data == "bosses":
        send_update(call, "📍 Выберите категорию боссов:", "bosses", get_bosses_kb())
    elif call.data == "b_bespredel":
        send_update(call, TEXTS["bosses_bespredel"], "bosses", get_back_kb("bosses"))
    elif call.data == "b_vertuhai":
        send_update(call, TEXTS["bosses_vertuhai"], "bosses", get_back_kb("bosses"))
    elif call.data == "sklad":
        send_update(call, TEXTS["sklad"], "sklad", get_back_kb("to_main"))
    elif call.data == "thanks":
        bot.answer_callback_query(call.id, "Раздел благодарности обновляется")

# ========== ЗАПУСК ==========
@app.route('/')
def home(): return "OK"

def run():
    bot.delete_webhook(drop_pending_updates=True)
    bot.polling(none_stop=True)

if __name__ == '__main__':
    Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))).start()
    run()
