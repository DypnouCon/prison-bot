import telebot
import os
import logging
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice
from flask import Flask
from threading import Thread

# ========== НАСТРОЙКИ ==========
BOT_TOKEN = '8025037882:AAGg047cDKMWDF_w4pUh3H5qFfSBChJIkFo'
# Для звезд нужен Payment Token (получи у BotFather -> /payments -> Сбер или ЮKassa не нужны, выбери "Telegram Stars")
PAYMENT_TOKEN = '' 

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask('')

# ========== ТЕКСТЫ ГАЙДОВ (СТРУКТУРИРОВАНО) ==========

TEXTS = {
    "start": "👋 **Привет! Я The Prison Helper.**\n\nВыбери нужный раздел гайда или поддержи автора проекта.",
    "energy": "⚡️ **ГАЙД ПО ЭНЕРГИИ**\n\n**📦 База:**\n• Стандарт: 50 ед.\n\n**💪 Усиления:**\n• 🏅 *Олимпиец:* +12 (Сет Олимпиец)\n• 🕶 *Лихой:* +20 (Сет лихие 90)\n• 🐺 *Вой:* +15 (Сет Оборотень)\n\n**👕 Шмотки (Посылки):**\n• Американец: +30\n• Дошик: +20\n• F1: +10\n\n**🧠 Таланты:**\n• Адреналин: +40\n• Второе дыхание: +70",
    "finka": "🗡 **ПРОКАЧКА ФИНКИ**\n\nВыбери подраздел для детальной информации:",
    "finka_tattoos": "✍️ **НАКОЛКИ (ФИНКА)**\n\n• 🦴 **Кости (+225):** Тюрьма 'Кресты'. Верх — день, низ — ночь.\n• 👸 **Принцесса (+80):** Выпадает в Катале.\n• 🐻 **Медведь (+20):** Слепой Кольщик.\n• ⛩ **Храм Мертвых (+70):** Комбо с Авто. Махно.",
    "samopal": "🔫 **УЛЬТИМАТИВНЫЙ САМОПАЛ**\n\n**💀 Тюрьмы (+230):**\n• *А. Централ (Отелло):* день +38 / ночь +112\n• *Остальные тюрьмы:* по +10 за сет.\n\n**🎰 Азарт (+590):**\n• *Покер:* Дьявольская удача (+400)\n• *Катала:* Падший Ангел (+90)\n\n**⛔️ Боссы (+1245):**\n• *Дюбель (Авто):* +300\n• *Дядя Миша (Блат):* +210",
    "thanks": "💎 **БЛАГОДАРНОСТЬ**\n\nВы можете поддержать проект двумя способами:\n\n1. 📦 **В игре:** Прислать 'Посылку с рублями' на ID `428871585`.\n2. ⭐ **В Telegram:** Нажать кнопку ниже и отправить Звезды."
}

# ========== КЛАВИАТУРЫ (ИНЛАЙН) ==========

def menu_main():
    kb = InlineKeyboardMarkup(row_width=2)
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

def menu_thanks():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("👨‍💻 Связь с Автором", url="https://t.me/gbg_georg"),
        InlineKeyboardButton("⭐ Поддержать Звездами (50)", callback_data="donate_stars"),
        InlineKeyboardButton("⬅️ Назад", callback_data="back_main")
    )
    return kb

# ========== ОБРАБОТЧИКИ ==========

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, TEXTS["start"], reply_markup=menu_main(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "energy":
        bot.edit_message_text(TEXTS["energy"], call.message.chat.id, call.message.message_id, 
                              reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Назад", callback_data="back_main")), 
                              parse_mode="Markdown")
    
    elif call.data == "finka":
        bot.edit_message_text(TEXTS["finka"], call.message.chat.id, call.message.message_id, reply_markup=menu_finka())

    elif call.data == "finka_tattoos":
        bot.edit_message_text(TEXTS["finka_tattoos"], call.message.chat.id, call.message.message_id, 
                              reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Назад", callback_data="finka")), 
                              parse_mode="Markdown")

    elif call.data == "samopal":
        bot.edit_message_text(TEXTS["samopal"], call.message.chat.id, call.message.message_id, 
                              reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Назад", callback_data="back_main")), 
                              parse_mode="Markdown")

    elif call.data == "thanks":
        bot.edit_message_text(TEXTS["thanks"], call.message.chat.id, call.message.message_id, reply_markup=menu_thanks())

    elif call.data == "back_main":
        bot.edit_message_text(TEXTS["start"], call.message.chat.id, call.message.message_id, reply_markup=menu_main())

    elif call.data == "donate_stars":
        # Отправка счета на 50 звезд
        bot.send_invoice(
            call.message.chat.id,
            title="Поддержка Prison Helper",
            description="Добровольное пожертвование звезд автору гайда",
            provider_token="", # Оставить пустым для Stars
            currency="XTR",
            prices=[LabeledPrice(label="Донат", amount=50)],
            invoice_payload="stars_donate"
        )

# Ответ на успешный платеж
@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# ========== СЕРВЕР ==========

@app.route('/')
def home(): return "I am alive"

def run_http():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    Thread(target=run_http).start()
    bot.polling(none_stop=True)
