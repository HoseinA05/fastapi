from telebot import types
from bot.utils.auth import is_authenticated


def register(bot):
    @bot.message_handler(commands=["start"])
    def start_handler(message):
        if is_authenticated(message.from_user.id):
            bot.send_message(
                message.chat.id, "authorized user! Welcome.")
        else:
            bot.send_message(
                message.chat.id, "Welcome! Use buttons to fetch from database.")

        markup = types.ReplyKeyboardMarkup(
            row_width=2, one_time_keyboard=True, resize_keyboard=True)
        btn1 = types.KeyboardButton("Show Students")
        btn2 = types.KeyboardButton("Show Teachers")
        btn3 = types.KeyboardButton("Show Courses")
        btn4 = types.KeyboardButton("Show Tag")
        btn5 = types.KeyboardButton("Show Categories")
        markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.reply_to(message, "Use buttons to fetch from database.",
                     reply_markup=markup)

    @bot.message_handler(func=lambda message: message.text in ["Show Courses", "Show Tag", "Show Categories"])
    def handle_test_options(message):
        option = message.text
        bot.send_message(message.chat.id, f"You selected: {option}")
