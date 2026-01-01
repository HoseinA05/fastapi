from telebot import TeleBot, types
from database.models import Courses
from bot.utils.crud_helpers import create_entity_markup
from bot.utils.formatters import format_course_info
from bot.handlers.start import startMarkup

# TODO: Add Option for selecting Teacher in a more user-friendly way (name instead of ID) + pagination for it.
# TODO: Add Buttons for offering multiple choices for fields like language and difficulty.


def register(bot: TeleBot):
    cancelMarkup = types.InlineKeyboardMarkup()
    cancelMarkup.add(types.InlineKeyboardButton(
        "Cancel", callback_data="cancel"))

    COURSE_FIELDS = [
        ('name', "the course's name"),
        ('teacher_id', "The course's Teacher ID"),
        ('description', "description (<Optional>)"),
        ('language', "language ('english', 'spanish', 'german', 'french', 'persian')"),
        ('difficulty', "difficulty (<Optional>) ('beginner', 'intermediate', 'expert')"),
    ]
    EDITABLE_FIELDS = {
        'name': 1,
        'description': 5,
        'difficulty': 6,
        'language': 7
    }

    # Showing details of a Course
    @bot.callback_query_handler(func=lambda call: call.data.startswith('course_'))
    def show_course_details(call):
        course_id = call.data.split('_')[1]
        course = Courses.getCourseById(course_id)

        if not course:
            bot.send_message(call.message.chat.id, "Course not found.")
            return

        details = format_course_info(course)
        markup = create_entity_markup("course", course_id)
        markup.add(types.InlineKeyboardButton(
            f"👨‍🏫 Teacher's Info", callback_data=f"teacher_{course[3]}"))

        bot.send_message(call.message.chat.id, details,
                         reply_markup=markup, parse_mode="HTML")

        bot.answer_callback_query(call.id)

    # Creating a Course Flow
    @bot.callback_query_handler(func=lambda call: call.data == 'create_course')
    def start_course_creation(call):
        msg = bot.send_message(call.message.chat.id,
                               "Please enter following data: (enter any key to start)",
                               reply_markup=cancelMarkup)
        bot.register_next_step_handler(msg, collect_field, {}, 0)
        bot.answer_callback_query(call.id)

    def collect_field(message, data, step):
        # Save previous field
        if step > 0:
            field_name = COURSE_FIELDS[step - 1][0]
            data[field_name] = message.text

        # Done collecting?
        if step >= len(COURSE_FIELDS):
            show_confirmation(message, data)
            return

        # Ask next question
        field_name, prompt = COURSE_FIELDS[step]
        msg = bot.send_message(message.chat.id, f"Now enter {prompt}:",
                               reply_markup=cancelMarkup)
        bot.register_next_step_handler(msg, collect_field, data, step + 1)

    def show_confirmation(message, data):
        summary = "Is this correct? (enter any key to continue or cancel to exit)\n\n" + "\n".join(
            f"{name.replace('_', ' ').title()}: {data[name]}"
            for name, _ in COURSE_FIELDS
        )
        msg = bot.send_message(message.chat.id, summary,
                               reply_markup=cancelMarkup)
        bot.register_next_step_handler(msg, create_course, data)

    def create_course(message, data):
        if Courses.createCourse(**data):
            bot.send_message(message.chat.id, "✅ Teacher created!",
                             reply_markup=startMarkup())
        else:
            bot.send_message(
                message.chat.id, "❌ Failed to create course.", reply_markup=startMarkup())

    # Editing a Course Flow
    @bot.callback_query_handler(func=lambda call: call.data.startswith('edit_course_'))
    def start_course_editing(call):
        course_id = call.data.split('_')[2]
        course = Courses.getCourseById(course_id)

        if not course:
            bot.send_message(call.message.chat.id, "Course not found.")
            bot.answer_callback_query(call.id)
            return

        editMarkup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True)
        for field in list(EDITABLE_FIELDS.keys()) + ['Cancel']:
            editMarkup.add(types.KeyboardButton(field.capitalize()))

        msg = bot.send_message(call.message.chat.id,
                               "Please enter the field you want to edit: ", reply_markup=editMarkup)

        bot.register_next_step_handler(
            msg, process_field_select, course)
        bot.answer_callback_query(call.id)

    def process_field_select(message, course: tuple):
        field = message.text.lower()
        if field == 'cancel' or field not in EDITABLE_FIELDS:
            msg = "Action cancelled." if field == 'cancel' else "Invalid field. Action cancelled."
            bot.send_message(message.chat.id, msg,
                             reply_markup=startMarkup())
            return

        current_value = course[EDITABLE_FIELDS[field]]

        msg = bot.send_message(
            message.chat.id, f"Current value is: {current_value}.\n Please enter new value for {field}:", reply_markup=cancelMarkup)
        bot.register_next_step_handler(
            msg, process_value_edit, course[0], field, current_value)

    def process_value_edit(message, course_id, field, previous_value):
        new_value = message.text

        # Handle cancellation
        if new_value.lower() == 'cancel' or new_value == f"{previous_value} (current)":
            msg = "Action cancelled." if new_value.lower(
            ) == 'cancel' else f"No changes made to {field}."
            bot.send_message(message.chat.id, msg, reply_markup=startMarkup())
            return

        # Update teacher
        if Courses.updateCourse(course_id, **{field: new_value}):
            bot.send_message(
                message.chat.id, f"✅ Course's {field} updated successfully.", reply_markup=startMarkup())
        else:
            bot.send_message(
                message.chat.id, f"❌ Failed to update Course's {field}.", reply_markup=startMarkup())

    # Deleting a Teacher
    @bot.callback_query_handler(func=lambda call: call.data.startswith('delete_course_'))
    def delete_course(call):
        course_id = call.data.split('_')[2]
        if (Courses.deleteCourse(course_id)):
            bot.send_message(call.message.chat.id, "✅ Course deleted.",
                             reply_markup=startMarkup())
        else:
            bot.send_message(call.message.chat.id, "❌ Failed to delete Course.",
                             reply_markup=startMarkup())
        bot.answer_callback_query(call.id)
