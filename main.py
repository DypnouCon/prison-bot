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

# ========== ТЕКСТЫ ГАЙДОВ (ОПТИМИЗИРОВАННЫЕ) ==========

TEXTS = {
    "start": (
        "📍 Главное меню\n\n"
        "The Prison Helper — информационный справочник по игре.\n\n"
        "Выберите раздел ниже для изучения деталей."
    ),
    
    "energy": (
        "📍 Главное меню » Энергия\n\n"
        "Базовый показатель: 50 ед.\n\n"
        "Постоянные усиления:\n"
        "• Талант Второе дыхание: +70\n"
        "• Талант Адреналин: +40\n"
        "• Сет Робин Гуд: +39 (все слоты)\n\n"
        "Предметы и сеты:\n"
        "• Комплект Олимпиец: +12\n"
        "• Сет Лихие 90: +20\n"
        "• Сет Оборотень: +15\n\n"
        "Мастера и одежда:\n"
        "• Сева 7 ур: +10\n"
        "• Ванька 10 ур: +10\n"
        "• Комплект Американец: +30"
    ),

    "finka_main": (
        "📍 Главное меню » Финка\n\n"
        "Выберите категорию предметов:"
    ),

    "finka_tats": (
        "📍 Главное меню » Финка » Наколки\n\n"
        "Кости: +225\n"
        "Добыча: Тюрьма Кресты (День — верх, Ночь — низ)\n\n"
        "Метки Судьбы: +180\n"
        "Добыча: Комбо-бой Авторитетный Шайба\n\n"
        "Пленник: +180\n"
        "Добыча: Босс Пацанский Дядя Миша\n\n"
        "Зверинец: +80\n"
        "Добыча: Магазин (игровая валюта)"
    ),

    "finka_wear": (
        "📍 Главное меню » Финка » Шмотки\n\n"
        "Ганнибал: +180\n"
        "Добыча: Босс Авторитетный Хирург\n\n"
        "Опасный: +150\n"
        "Добыча: Босс Пацанский Хирург\n\n"
        "Якудза: +40\n"
        "Добыча: Босс Блатной Бурят\n\n"
        "Армани: +35\n"
        "Добыча: Локация Угольки"
    ),

    "samopal": (
        "📍 Главное меню » Самопал\n\n"
        "Урон от Боссов:\n"
        "• Дюбель Авто: +300\n"
        "• Дядя Миша Блат: +210\n"
        "• Шайба Авто: +160\n\n"
        "Азартные игры:\n"
        "• Покер Дьявольская удача: +400\n"
        "• Катала Падший Ангел: +90\n"
        "• Колесо фортуны: +50\n\n"
        "Мастера:\n"
        "• Янка Обряд: +80\n"
        "• Кеша Толстосум: +40\n"
        "• Сет Тлен: +90 (все мастера)"
    ),

    "thanks": (
        "📍 Главное меню » Благодарность\n\n"
        "ID для посылок в игре: 428871585\n\n"
        "Вы также можете поддержать проект Звездами Телеграм."
    )
}

# ========== КЛАВИАТУРЫ ==========

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
    bot.send_message(message.chat.id, "Загрузка меню...", reply_markup=ReplyKeyboardRemove())
    bot.send_message(message.chat.id, TEXTS["start"], reply_markup=get_main_kb())

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "to_main":
        bot.edit_message_text(TEXTS["start"], call.message.chat.id, call.message.message_id, reply_markup=get_main_kb())
    
    elif call.data == "energy":
        bot.edit_message_text(TEXTS["energy"], call.message.chat.id, call.message.message_id, reply_markup=get_back_kb("to_main"))
        
    elif call.data == "finka":
        bot.edit_message_text(TEXTS["finka_main"], call.message.chat.id, call.message.message_id, reply_markup=get_finka_kb())
        
    elif call.data == "finka_tats":
        bot.edit_message_text(TEXTS["finka_tats"], call.message.chat.id, call.message.message_id, reply_markup=get_back_kb("finka"))
        
    elif call.data == "finka_wear":
        bot.edit_message_text(TEXTS["finka_wear"], call.message.chat.id, call.message.message_id, reply_markup=get_back_kb("finka"))
        
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

# ========== ЗАПУСК ==========

@app.route('/')
def home(): return "OK"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    Thread(target=run).start()
    bot.polling(none_stop=True)
