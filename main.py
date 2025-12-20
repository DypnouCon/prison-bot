import telebot
import os
import logging
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice
from flask import Flask
from threading import Thread

# ========== НАСТРОЙКИ ==========
BOT_TOKEN = '8025037882:AAGg047cDKMWDF_w4pUh3H5qFfSBChJIkFo'
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask('')

# ========== ПОДРОБНАЯ БАЗА ДАННЫХ ==========

TEXTS = {
    "start": "👤 **The Prison Helper**\n\nИнформационный ресурс по игре The Prison. Выберите интересующий раздел для получения подробных данных по прокачке и предметам.",
    
    "energy": (
        "⚡️ **ЭНЕРГИЯ: ПОЛНЫЙ СПИСОК УСИЛЕНИЙ**\n\n"
        "**Постоянные бонусы:**\n"
        "• Талант 'Второе дыхание': +70 ед.\n"
        "• Талант 'Адреналин': +40 ед.\n"
        "• Сет 'Робин Гуд': +39 за все слоты (покупается у Барыги).\n\n"
        "**Комплекты (усиления на выбор):**\n"
        "• Олимпиец: +12 (выпадает в посылках).\n"
        "• Лихой: +20 (Слепой Кольщик, сет 'Лихие 90').\n"
        "• Вой: +15 (Слепой Кольщик, сет 'Оборотень').\n\n"
        "**Одежда и Мастера:**\n"
        "• Пирожок: +10 (Мастер Сева, требуется 7 уровень).\n"
        "• Четки Ванька: +10 (Мастер Ванька, требуется 10 уровень).\n"
        "• Американец: +30 (выпадает из посылок, нужно 3 вещи).\n"
        "• Дошик: +20 (выпадает из посылок).\n"
        "• Комплекты F1, Монетница, Радио: по +10 каждый."
    ),

    "finka_main": "🗡 **ГАЙД ПО ФИНКЕ**\n\nВыберите категорию для изучения способов получения урона:",

    "finka_tattoos": (
        "✍️ **НАКОЛКИ НА ФИНКУ**\n\n"
        "• **Кости (+225):** Тюрьма 'Кресты'. Верхняя часть выпадает в дневных движухах, нижняя — в ночных.\n"
        "• **Метки Судьбы (+180):** Выпадает при победе в комбо-бою с Авторитетным Шайбой.\n"
        "• **Пленник (+180):** Выпадает с босса Пацанский Дядя Миша.\n"
        "• **Восток (+160):** Выпадает с босса Пацанский Бурят.\n"
        "• **Принцесса (+80):** Можно выиграть в 'Катале'.\n"
        "• **Мафиози (+80):** Редкий сет у Слепого Кольщика.\n"
        "• **Храм Мертвых (+70):** Комбо-бой с Авторитетным Махно.\n"
        "• **Череп и Роза / Медведь:** по +20 (Слепой Кольщик).\n"
        "• **Зверинец (+80):** Покупается за игровую валюту в магазине."
    ),

    "finka_clothes": (
        "👕 **ЭКИПИРОВКА НА ФИНКУ**\n\n"
        "• **Ганнибал (+180):** Выпадает с босса Авторитетный Хирург.\n"
        "• **Опасный (+150):** Выпадает с босса Пацанский Хирург.\n"
        "• **Якудза (+40):** Выпадает с босса Блатной Бурят.\n"
        "• **Старье (+30):** Самый простой сет, падает с Махно.\n\n"
        "**Движухи в тюрьмах:**\n"
        "• Армани (+35): локация 'Угольки'.\n"
        "• Кельвин Кляйн (+30): локация 'Кресты'.\n"
        "• D&G (+25): локация 'Лефортовка'.\n"
        "• Гучи / Гермес (+20): Крытка и Централ.\n\n"
        "**Спец. предметы:**\n"
        "• Швейцарский нож / Крюк: +20 / +10 (запрещенные посылки)."
    ),

    "samopal": (
        "🔫 **САМОПАЛ: МАКСИМАЛЬНЫЙ УРОН**\n\n"
        "**Боссы (основной прирост):**\n"
        "• Дюбель (Авто): +300 урона.\n"
        "• Дядя Миша (Блат): +210 урона.\n"
        "• Шайба (Авто): +160 урона.\n"
        "• Близнецы: +150 урона.\n\n"
        "**Азартные игры:**\n"
        "• Покер: сет 'Дьявольская удача' (+400).\n"
        "• Катала: сет 'Падший Ангел' (+90).\n"
        "• Колесо фортуны: сеты 'Жмурки' и 'Знаток удачи' (по +50).\n\n"
        "**Мастера:**\n"
        "• Янка: сет 'Обряд' (+80).\n"
        "• Кеша: сет 'Толстосум' (+40).\n"
        "• Паша Лесник: +30.\n"
        "• Сборный сет 'Тлен': +90 (нужно прокачать всех мастеров от Яши до Нинки)."
    ),

    "thanks": (
        "💎 **ПОДДЕРЖКА ПРОЕКТА**\n\n"
        "Если гайд оказался полезным, вы можете отблагодарить автора:\n\n"
        "1. **В игре:** Отправьте 'Посылку с рублями' игроку ID `428871585`.\n"
        "2. **Звезды:** Нажмите кнопку ниже для пожертвования через Telegram Stars."
    )
}

# ========== КЛАВИАТУРЫ ==========

def menu_main():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("⚡️ ЭНЕРГИЯ", callback_data="energy"),
        InlineKeyboardButton("🗡 ФИНКА", callback_data="finka"),
        InlineKeyboardButton("🔫 САМОПАЛ", callback_data="samopal"),
        InlineKeyboardButton("💎 БЛАГОДАРНОСТЬ", callback_data="thanks")
    )
    return kb

def menu_finka():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("✍️ Наколки", callback_data="finka_tattoos"),
        InlineKeyboardButton("👕 Шмотки", callback_data="finka_clothes"),
        InlineKeyboardButton("⬅️ Назад", callback_data="back_main")
    )
    return kb

def menu_back(target):
    return InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Назад", callback_data=target))

# ========== ОБРАБОТЧИКИ ==========

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, TEXTS["start"], reply_markup=menu_main())

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    # Логика переключения экранов
    if call.data == "back_main":
        bot.edit_message_text(TEXTS["start"], call.message.chat.id, call.message.message_id, reply_markup=menu_main())
    
    elif call.data == "energy":
        bot.edit_message_text(TEXTS["energy"], call.message.chat.id, call.message.message_id, reply_markup=menu_back("back_main"))
        
    elif call.data == "finka":
        bot.edit_message_text(TEXTS["finka_main"], call.message.chat.id, call.message.message_id, reply_markup=menu_finka())
        
    elif call.data == "finka_tattoos":
        bot.edit_message_text(TEXTS["finka_tattoos"], call.message.chat.id, call.message.message_id, reply_markup=menu_back("finka"))
        
    elif call.data == "finka_clothes":
        bot.edit_message_text(TEXTS["finka_clothes"], call.message.chat.id, call.message.message_id, reply_markup=menu_back("finka"))
        
    elif call.data == "samopal":
        bot.edit_message_text(TEXTS["samopal"], call.message.chat.id, call.message.message_id, reply_markup=menu_back("back_main"))
        
    elif call.data == "thanks":
        kb = InlineKeyboardMarkup(row_width=1)
        kb.add(
            InlineKeyboardButton("✉️ Связь с автором", url="https://t.me/gbg_georg"),
            InlineKeyboardButton("⭐ Поддержать (50 Stars)", callback_data="donate_stars"),
            InlineKeyboardButton("⬅️ Назад", callback_data="back_main")
        )
        bot.edit_message_text(TEXTS["thanks"], call.message.chat.id, call.message.message_id, reply_markup=kb)

    elif call.data == "donate_stars":
        bot.send_invoice(
            call.message.chat.id,
            title="Поддержка Prison Helper",
            description="Добровольное пожертвование",
            provider_token="",
            currency="XTR",
            prices=[LabeledPrice(label="Донат", amount=50)],
            invoice_payload="stars_donate"
        )

@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# ========== СЕРВЕР ==========

@app.route('/')
def home(): return "Бот работает"

def run_http():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    Thread(target=run_http).start()
    bot.polling(none_stop=True)
