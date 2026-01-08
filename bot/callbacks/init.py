from . import students, teachers, courses, tags, categories
from bot.handlers.start import startMarkup

# TODO: Create a new entity for Reviews (Change The Corresponding codes from courses and students to use that)
# TODO: Add Option for handling all updates at once.


def register_all_callbacks(bot):
    """Register all callback handlers"""
    students.register(bot)
    teachers.register(bot)
    courses.register(bot)
    tags.register(bot)
    categories.register(bot)

    # Cancel is common among all
    @bot.callback_query_handler(func=lambda call: call.data == 'cancel')
    def cancel_action(call):
        bot.clear_step_handler(call.message)
        bot.send_message(call.message.chat.id,
                         "Action cancelled.", reply_markup=startMarkup())
        bot.answer_callback_query(call.id)
