from . import students, teachers, courses, tags
from bot.handlers.start import startMarkup


def register_all_callbacks(bot):
    """Register all callback handlers"""
    students.register(bot)
    teachers.register(bot)
    courses.register(bot)
    tags.register(bot)

    # Cancel is common among all
    @bot.callback_query_handler(func=lambda call: call.data == 'cancel')
    def cancel_action(call):
        bot.clear_step_handler(call.message)
        bot.send_message(call.message.chat.id,
                         "Action cancelled.", reply_markup=startMarkup())
        bot.answer_callback_query(call.id)
