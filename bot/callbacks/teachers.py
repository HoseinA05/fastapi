from telebot import types
from database.models import Teachers
from bot.utils.formatters import format_teacher_info


def register(bot):
    @bot.callback_query_handler(func=lambda call: call.data.startswith('teacher_'))
    def show_teacher_details(call):
        teacher_id = call.data.split('_')[1]
        teacher = Teachers.getTeachertById(teacher_id)

        if teacher:
            details = format_teacher_info(teacher)
            markup = types.InlineKeyboardMarkup()
            bot.send_message(call.message.chat.id, details,
                             reply_markup=markup, parse_mode="HTML")
        else:
            bot.send_message(call.message.chat.id, "Teacher not found.")

        bot.answer_callback_query(call.id)
