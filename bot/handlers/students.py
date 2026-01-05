import logging
from telebot import types, TeleBot
from database.models import Students, Admins

logger = logging.getLogger(__name__)


def register(bot: TeleBot):
    @bot.message_handler(func=lambda message: message.text == "Show Students")
    def get_students(message):
        if not Admins.is_authenticated(message.from_user.id):
            bot.send_message(
                message.chat.id, "⛔ Unauthorized access!\nPlease /login first.")
            return

        try:
            data = Students.getAllStudents()
            if data:
                markup = types.InlineKeyboardMarkup(row_width=2)

                for row in data:
                    btn = types.InlineKeyboardButton(
                        f"@{row[1]} | id#{row[0]}", callback_data=f"student_{row[0]}")
                    markup.add(btn)

                # add button for creating a new student
                markup.add(types.InlineKeyboardButton(
                    "➕ Create New Student 🔒", callback_data="create_student"))

                bot.send_message(
                    message.chat.id, "Here is the data:", reply_markup=markup)
            else:
                markup = types.InlineKeyboardMarkup(row_width=1)
                markup.add(types.InlineKeyboardButton(
                    "➕ Create New Student 🔒", callback_data="create_student"))
                bot.reply_to(message, "No data found.", reply_markup=markup)
        except Exception as e:
            logger.error(f"Error in get_students handler: {e}")
            bot.reply_to(message, "Sorry, an error occurred.")
