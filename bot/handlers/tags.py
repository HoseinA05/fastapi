import logging
from telebot import types, TeleBot
from database.models import Tags

logger = logging.getLogger(__name__)


def register(bot: TeleBot):
    @bot.message_handler(func=lambda message: message.text == "Show Tags")
    def get_tags(message):
        try:
            data = Tags.getAllTags()
            if data:
                markup = types.InlineKeyboardMarkup(row_width=2)

                for row in data:
                    btn = types.InlineKeyboardButton(
                        f"{row[1]} | id#{row[0]}", callback_data=f"tag_{row[0]}")
                    markup.add(btn)

                # add button for creating a new tag
                markup.add(types.InlineKeyboardButton(
                    "➕ Create New Tag", callback_data="create_tag"))

                bot.send_message(
                    message.chat.id, "Here is the data:", reply_markup=markup)
            else:
                markup = types.InlineKeyboardMarkup(row_width=1)
                markup.add(types.InlineKeyboardButton(
                    "➕ Create New Tag", callback_data="create_tag"))

                bot.reply_to(message, "No data found.", reply_markup=markup)
        except Exception as e:
            logger.error(f"Error in 'Show Tags' handler: {e}")
            bot.reply_to(message, "Sorry, an error occurred.")
