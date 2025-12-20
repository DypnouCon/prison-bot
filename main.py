import telebot
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from flask import Flask
from threading import Thread

# ========== НАСТРОЙКИ ==========
BOT_TOKEN = '8025037882:AAGg047cDKMWDF_w4pUh3H5qFfSBChJIkFo'
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask('')

# Ссылка на новую картинку welcome.png
START_IMG = "https://raw.githubusercontent.com/DypnouCon/prison-bot/main/welcome.png"

# ========== ТЕКСТЫ ГАЙДОВ ==========
TEXTS = {
    "start": (
        "🆕 **Обновление бота!** Если меню не отображается, введите /start\n\n"
        "👋 **Рады видеть тебя в нашем кругу, дружище!**\n\n"
        "Ты зашел в Prison Helper — место, где мы по крупицам собираем всё, что поможет тебе "
        "стать авторитетнее и сильнее в мире «The Prison». Этот бот — твой верный напарник: "
        "подскажет, где выбить нужную наколку и как не слить ресурсы впустую.\n\n"
        "Чувствуй себя как дома. Осматривайся, изучай гайды. Удачного фарма! 👊"
    ),
    
    "poison": (
        "📍 **Главное меню » 🧪 Яд**\n"
        "— — — — — — — — — —\n"
        "Яд работает независимо от Финки и Самопала. Это твой «джокер» для победы над сильными противниками.\n\n"
        "🧬 **Прокачка Химии:**\n"
        "• Талант 'Химик': Базовое усиление.\n"
        "• Мастер Ашот (10 ур.): Максимальный бонус к флаконам.\n\n"
        "👕 **Сеты на Яд:**\n"
        "• Чумной Доктор: +12% урона.\n"
        "• Лаборант: Шанс крита.\n\n"
        "💡 *Совет: Копи яд для серьезных рейдов (Дюбель, Гром и выше).* "
    ),

    "energy": (
        "📍 **Главное меню » ⚡️ Энергия**\n"
        "— — — — — — — — — —\n"
        "🔋 **База:** 50 ед.\n\n"
        "🧬 **Таланты:** Второе дыхание (+70), Адреналин (+40).\n\n"
        "👕 **Комплекты:**\n"
        "• Американец: +30 ед.\n"
        "• Дошик: +20 ед.\n"
        "• Пирожок (Сева 7 ур.): +10 ед.\n"
        "• Четки (Ванька 10 ур.): +10 ед."
    ),

    "finka_main": "📍 **Главное меню » 🗡 Финка**\n\nВыберите категорию для усиления личного урона:",

    "finka_tats": (
        "📍 **Финка » ✍️ Наколки**\n"
        "— — — — — — — — — —\n"
        "🦴 **Комплект 'Кости' (+225)**\n"
        "• 12 наколок. Локация: Кресты.\n\n"
        "👁 **Метки Судьбы (+180)**\n"
        "• 34 наколки. Босс: Авто-Шайба.\n\n"
        "🐯 **Комплект 'Зверинец' (+80)**\n"
        "• 10 наколок. Магазин."
    ),

    "finka_wear": (
        "📍 **Финка » 👕 Экипировка**\n"
        "— — — — — — — — — —\n"
        "👺 **Сет 'Ганнибал' (+180)**\n"
        "• Босс: Авто-Хирург.\n\n"
        "🔪 **Сет 'Опасный' (+150)**\n"
        "• Босс: Пац-Хирург.\n\n"
        "🏙 **Движухи:** Армани (+35), К.Кляйн (+30), D&G (+25)."
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
    )
}

# ========== КЛАВИАТУРЫ ==========
def kb_main():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("⚡️ Энергия", callback_data="energy"),
        InlineKeyboardButton("🗡 Финка", callback_data="finka"),
        InlineKeyboardButton("🔫 Самопал", callback_data="samopal"),
        InlineKeyboardButton("🧪 Яд", callback_data="poison"),
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

# ========== ОБРАБОТЧИКИ ==========
@bot.message_handler(commands=['start'])
def start(message):
    print(f"User {message.chat.id} started the bot") # Пункт А: Логирование
    bot.send_photo(message.chat.id, START_IMG, caption=TEXTS["start"], reply_markup=kb_main(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    cid, mid = call.message.chat.id, call.message.message_id
    print(f"User {cid} pressed {call.data}") # Пункт А: Логирование
    
    def edit(text, kb):
        try: 
            # Пункт А: Обработка ошибок (чтобы не падал при повторном нажатии на ту же кнопку)
            bot.edit_message_caption(text, cid, mid, reply_markup=kb, parse_mode="Markdown")
        except telebot.apihelper.ApiTelegramException as e:
            if "message is not modified" not in e.description:
                raise e

    if call.data == "to_main": edit(TEXTS["start"], kb_main())
    elif call.data == "energy": edit(TEXTS["energy"], InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Назад", callback_data="to_main")))
    elif call.data == "finka": edit(TEXTS["finka_main"], kb_finka())
    elif call.data == "f_tats": edit(TEXTS["finka_tats"], InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Назад", callback_data="finka")))
    elif call.data == "f_wear": edit(TEXTS["finka_wear"], InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Назад", callback_data="finka")))
    elif call.data == "samopal": edit(TEXTS["samopal"], InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Назад", callback_data="to_main")))
    elif call.data == "poison": edit(TEXTS["poison"], InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Назад", callback_data="to_main")))
    elif call.data == "bosses": edit("📍 **Раздел: Боссы**\nВыберите группировку:", kb_bosses())
    elif call.data == "b_bespredel": edit("🔘 **Беспредельщики**\n\nШайба: 50к/150к/300к\nД.Миша: 3м/9м/18м\nХирург: 30м/90м/180м\nТротил: 200м/600м/1.2б", InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Назад", callback_data="bosses")))
    elif call.data == "b_vertuhai": edit("🔘 **Вертухаи**\n\nПалыч: 100к\nБлизнецы: 2м\nБорзов: 3м/9м/18м\nДюбель: 40м/120м/240м\nГром: 70м/210м/420м", InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Назад", callback_data="bosses")))
    elif call.data == "sklad": edit("📦 **Склад**\n\nРаздел находится в доработке. Здесь будут советы по ресурсам и отзывы игроков.", InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Назад", callback_data="to_main")))
    elif call.data == "thanks": bot.answer_callback_query(call.id, "Раздел в разработке")

# ========== ЗАПУСК ==========
@app.route('/')
def home(): return "OK"

if __name__ == '__main__':
    Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()
    bot.delete_webhook(drop_pending_updates=True)
    bot.polling(none_stop=True)
