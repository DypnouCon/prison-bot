import telebot
import os
import logging
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice, ReplyKeyboardRemove
from flask import Flask
from threading import Thread

# ========== НАСТРОЙКИ ==========
BOT_TOKEN = '8025037882:AAGg047cDKMWDF_w4pUh3H5qFfSBChJIkFo'
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask('')

# ========== ТЕКСТЫ ГАЙДОВ ==========

TEXTS = {
    "start": "👤 **The Prison Helper**\n\nИнформационный ресурс по игре. Всё управление осуществляется через кнопки под сообщениями.",
    
    "energy": (
        "⚡️ **Гайд по энергии**\n\n"
        "• **База:** 50 ед.\n"
        "• **Таланты:** Второе дыхание (+70), Адреналин (+40).\n"
        "• **Сеты:** Робин Гуд (+39), Олимпиец (+12), Лихой (+20), Вой (+15).\n"
        "• **Мастера:** Сева 7ур (+10), Ванька 10ур (+10).\n"
        "• **Посылки:** Американец (+30), Дошик (+20), F1 (+10)."
    ),

    "finka_main": "🗡 **Раздел: Финка**\n\nВыберите тип предметов для подробного описания:",

    "finka_tattoos": (
        "✍️ **Наколки на финку**\n\n"
        "• **Кости (+225):** Тюрьма 'Кресты'. Верх — день, низ — ночь.\n"
        "• **Метки Судьбы (+180):** Комбо-бой Авто. Шайба.\n"
        "• **Пленник (+180):** Босс Пац. Дядя Миша.\n"
        "• **Восток (+160):** Босс Пац. Бурят.\n"
        "• **Принцесса (+80):** Выигрыш в Катале.\n"
        "• **Зверинец (+80):** Покупка в магазине."
    ),

    "finka_clothes": (
        "👕 **Экипировка на финку**\n\n"
        "• **Ганнибал (+180):** Босс Авто. Хирург.\n"
        "• **Опасный (+150):** Босс Пац. Хирург.\n"
        "• **Якудза (+40):** Босс Блат. Бурят.\n"
        "• **Тюрьмы:** Армани (+35, Угольки), К.Кляйн (+30, Кресты), D&G (+25, Лефортовка)."
    ),

    "samopal": (
        "🔫 **Гайд по самопалу**\n\n"
        "• **Боссы:** Дюбель Авто (+300), Дядя Миша Блат (+210), Шайба Авто (+160).\n"
        "• **Азарт:** Покер (+400), Катала (+90), Колесо (+50).\n"
        "• **Мастера:** Янка (+80), Кеша (+40), Паша Лесник (+30), Сет 'Тлен' (+90)."
    ),

    "thanks": "💎 **Поддержка автора**\n\nID для посылок в игре: `428871585`.\nТакже вы можете поддержать проект звездами."
}

# ========== ИНЛАЙН КЛАВИАТУРЫ (ЕДИНЫЙ СТИЛЬ) ==========

def get_main_kb():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("⚡️ Энергия", callback_data="energy"),
        InlineKeyboardButton("🗡 Финка", callback_data="finka"),
        InlineKeyboardButton("🔫 Самопал", callback_data="samopal"),
        InlineKeyboardButton("💎 Благодарность", callback_data="thanks")
    )
    return kb

def get_finka_kb():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("✍️ Наколки", callback_data="finka_tats"),
        InlineKeyboardButton("👕 Шмотки", callback_data="finka_wear"),
        InlineKeyboardButton("⬅️ Назад", callback_data="to_main")
    )
    return kb

def get_back_kb(target):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("⬅️ Назад", callback_data=target))
    return kb

# ========== ОБРАБОТЧИКИ ==========

@bot.message_handler(commands=['start'])
def start_command(message):
    # ReplyKeyboardRemove() убирает старые кнопки с экрана клавиатуры
    bot.send_message(
        message.chat.id, 
        TEXTS["start"], 
        reply_markup=ReplyKeyboardRemove()
    )
    # Сразу отправляем сообщение с правильными Inline-кнопками
    bot.send_message(
        message.chat.id, 
        "Выберите раздел меню:", 
        reply_markup=get_main_kb()
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "to_main":
        bot.edit_message_text(TEXTS["start"], call.message.chat.id, call.message.message_id, reply_markup=get_main_kb())
    
    elif call.data == "energy":
        bot.edit_message_text(TEXTS["energy"], call.message.chat.id, call.message.message_id, reply_markup=get_back_kb("to_main"))
        
    elif call.data == "finka":
        bot.edit_message_text(TEXTS["finka_main"], call.message.chat.id, call.message.message_id, reply_markup=get_finka_kb())
        
    elif call.data == "finka_tats":
        bot.edit_message_text(TEXTS["finka_tattoos"], call.message.chat.id, call.message.message_id, reply_markup=get_back_kb("finka"))
        
    elif call.data == "finka_wear":
        bot.edit_message_text(TEXTS["finka_clothes"], call.message.chat.id, call.message.message_id, reply_markup=get_back_kb("finka"))
        
    elif call.data == "samopal":
        bot.edit_message_text(TEXTS["samopal"], call.message.chat.id, call.message.message_id, reply_markup=get_back_kb("to_main"))
        
    elif call.data == "thanks":
        kb = InlineKeyboardMarkup(row_width=1)
        kb.add(
            InlineKeyboardButton("✉️ Связь с автором", url="https://t.me/gbg_georg"),
            InlineKeyboardButton("⭐ Поддержать (50 Stars)", callback_data="pay_stars"),
            InlineKeyboardButton("⬅️ Назад", callback_data="to_main")
        )
        bot.edit_message_text(TEXTS["thanks"], call.message.chat.id, call.message.message_id, reply_markup=kb)

    elif call.data == "pay_stars":
        bot.send_invoice(
            call.message.chat.id,
            title="Донат Prison Helper",
            description="Поддержка развития бота",
            provider_token="",
            currency="XTR",
            prices=[LabeledPrice(label="Донат", amount=50)],
            invoice_payload="donate"
        )

@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# ========== ЗАПУСК СЕРВЕРА ==========

@app.route('/')
def home(): return "OK"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    Thread(target=run).start()
    bot.polling(none_stop=True)
