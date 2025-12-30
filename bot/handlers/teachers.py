import logging
from telebot import types
from database.models import Teachers

logger = logging.getLogger(__name__)


def register(bot):
    @bot.message_handler(func=lambda message: message.text == "Show Teachers")
    def get_teachers(message):
        try:
            data = Teachers.getAllTeachers()
            if data:

                markup = types.InlineKeyboardMarkup(row_width=2)
                for row in data:
                    btn = types.InlineKeyboardButton(
                        f"@{row[1]} | id#{row[0]}", callback_data=f"teacher_{row[0]}")
                    markup.add(btn)
                bot.send_message(
                    message.chat.id, "Here is the data:", reply_markup=markup)
            else:
                bot.reply_to(message, "No data found.")
        except Exception as e:
            logger.error(f"Error in get_teachers handler: {e}")
            bot.reply_to(message, "Sorry, an error occurred.")
