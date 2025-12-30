from telebot import types
from database.models import Students
from bot.utils.formatters import format_student_info


def register(bot):
    @bot.callback_query_handler(func=lambda call: call.data.startswith('student_'))
    def show_student_details(call):
        student_id = call.data.split('_')[1]
        student = Students.getStudentById(student_id)

        if student:
            details = format_student_info(student)
            markup = types.InlineKeyboardMarkup()
            bot.send_message(call.message.chat.id, details,
                             reply_markup=markup, parse_mode="HTML")
        else:
            bot.send_message(call.message.chat.id, "Student not found.")

        bot.answer_callback_query(call.id)
