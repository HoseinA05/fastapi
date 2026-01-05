import logging
from telebot import types
from database.models import Categories

logger = logging.getLogger(__name__)


def register(bot):
    @bot.message_handler(func=lambda message: message.text == "Show Categories")
    def get_categories(message):
        try:
            data = Categories.getAllCategories()
            if data:
                markup = types.InlineKeyboardMarkup(row_width=2)

                for row in data:
                    btn = types.InlineKeyboardButton(
                        f"{row[1]} | id#{row[0]}", callback_data=f"category_{row[0]}")
                    markup.add(btn)

                # add button for creating a new category
                markup.add(types.InlineKeyboardButton(
                    "➕ Create New Category", callback_data="create_category"))

                bot.send_message(
                    message.chat.id, "Here is the data:", reply_markup=markup)
            else:
                markup = types.InlineKeyboardMarkup(row_width=1)
                markup.add(types.InlineKeyboardButton(
                    "➕ Create New Category", callback_data="create_category"))

                bot.reply_to(message, "No data found.", reply_markup=markup)
        except Exception as e:
            logger.error(f"Error in 'Show Categories' handler: {e}")
            bot.reply_to(message, "Sorry, an error occurred.")
