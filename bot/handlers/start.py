from telebot import types

# TODO: Add Pagincation to Showing rows of entities (To all entities)


def register(bot):
    @bot.message_handler(commands=["start"])
    def start_handler(message):
        startMessage(bot, message=message)


def startMessage(bot, message):
    # if is_authenticated(message.from_user.id):
    #     bot.send_message(
    #         message.chat.id, "authorized user! Welcome.")

    markup = startMarkup()
    bot.reply_to(message, "Use buttons to fetch from database.",
                 reply_markup=markup)


def startMarkup():
    markup = types.ReplyKeyboardMarkup(
        row_width=2, one_time_keyboard=True, resize_keyboard=True)
    btn1 = types.KeyboardButton("Show Students")
    btn2 = types.KeyboardButton("Show Teachers")
    btn3 = types.KeyboardButton("Show Courses")
    btn4 = types.KeyboardButton("Show Tags")
    btn5 = types.KeyboardButton("Show Categories")
    markup.add(btn1, btn2, btn3, btn4, btn5)
    return markup
