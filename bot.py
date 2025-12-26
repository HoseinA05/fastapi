import os
import logging
from database.models import testModel
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

logger = logging.getLogger(__name__)

_bot = None

def get_bot():
    global _bot
    if _bot is None:
        import telebot
        BOT_TOKEN = os.environ.get("BOT_TOKEN")
        _bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
        
        @_bot.message_handler(commands=["start"])
        def start(message):
            _bot.reply_to(message, "Welcome! Use /getdata to fetch from database.")

        @_bot.message_handler(commands=["getdata"])
        def get_data(message):
            try:
                data = testModel.getAllUsers()
                if data:
                    _bot.reply_to(message, f"Data: {data}")

                    response = "";
                    for i in range(3):
                        response += "\n";
                        response += f"""
                        <b>📚 {data[i][0]}</b>
                        <i>نویسنده:</i> {data[i][1]}
                        <i>موجودی:</i> {data[i][3]}/{data[i][8]}
                        <code>کد: {data[i][1]}</code>
                        """
                    _bot.reply_to(message, response, parse_mode='HTML')
                else:
                    _bot.reply_to(message, "No data found or database error.")
            except Exception as e:
                logger.error(f"Error in getdata handler: {e}")
                _bot.reply_to(message, "Sorry, an error occurred.")
        
        @_bot.message_handler(func=lambda message: True)
        def echo_all(message):
            _bot.reply_to(message, f"You said: {message.text}")
    
    return _bot