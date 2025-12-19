import telebot
import time
import logging
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from flask import Flask
from threading import Thread

# ========== НАСТРОЙКИ ==========
BOT_TOKEN = '8025037882:AAGg047cDKMWDF_w4pUh3H5qFfSBChJIkFo'

bot = telebot.TeleBot(BOT_TOKEN)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ========== ВЕБ-СЕРВЕР (ЧТОБЫ НЕ СПАЛ) ==========
app = Flask('')

@app.route('/')
def home():
    return "I am alive"

def run_http():
    # Запускаем на порту 8080 или другом доступном
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_http)
    t.start()

# ========== ДАННЫЕ И ГАЙДЫ ==========
CREATOR = '@gbg_georg'
GAME_ID = '428871585'

GUIDES = {
    "⚡️ ЭНЕРГИЯ": """⚡️ **ПОЛНЫЙ ГАЙД ПО ЭНЕРГИИ**
• Стандартная энергия: 50
• Усиления: Олимпиец (+12), Лихой (+20), Вой (+15)
• Занычка: Робин Гуд (+3)
• Одежда: Американец (+30), Дошик (+20), Пирожок (+10) и др.
• Таланты: Адреналин (+40), Второе дыхание (+70)""",

    "🗡 ФИНКА": """🗡 **УЛЬТИМАТИВНЫЙ ГАЙД: ФИНКА**
👊 **Таланты:** Тихий Убийца (+10), Танец Лезвий (+1)
✍️ **Наколки:** Кости (+225), Пленник (+180), Восток (+160), Метки Судьбы (+180) и др.
👕 **Шмотки:** Опасный (+150), Ганнибал (+180), Якудза (+40) и др.""",

    "🔫 САМОПАЛ": """🔫 **УЛЬТИМАТИВНЫЙ ГАЙД: САМОПАЛ**
👀 **База:** 70 урона
💀 **Тюрьмы:** Отелло (+112), Хохот (+10)
💬 **Мастера:** Тлен (+90), Янка (+80), Кеша (+40)
🎁 **Посылки:** Птичка (+50), Спортивный (+45)
🎰 **Азарт:** Дьявольская удача (+400), Падший Ангел (+90)
⛔️ **Боссы:** Русь (+210), Совет (+160), Чикано (+150), Буйство (+300)""",

    "📞 ПОДДЕРЖКА": f"""📞 **СВЯЗЬ**
Создатель: {CREATOR}
ID: {GAME_ID}"""
}

# ========== ЛОГИКА ==========
def get_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*[KeyboardButton(name) for name in GUIDES.keys()])
    return markup

@bot.message_handler(commands=['start', 'help'])
def handle_start(message):
    bot.send_message(message.chat.id, "👋 Привет! Я The Prison Helper.", reply_markup=get_main_menu())

@bot.message_handler(func=lambda m: m.text in GUIDES)
def handle_guide(m):
    bot.send_message(m.chat.id, GUIDES[m.text], parse_mode='Markdown', reply_markup=get_main_menu())

# ========== ЗАПУСК ==========
if __name__ == '__main__':
    # Сначала запускаем веб-сервер в фоне
    keep_alive()
    # Потом запускаем бота
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logger.error(f"Error: {e}")
