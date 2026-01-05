from telebot import types, TeleBot
from database.models import Teachers
from bot.utils.formatters import format_teacher_info
from bot.handlers.start import startMarkup
from bot.utils.crud_helpers import create_entity_markup

# TODO: Add Buttons for skipping Optional Fields (Add to all entities).
# TODO: Add Option for handling all updates at once.
# TODO: Add Authentication for sensitive actions and info.

# TODO: Add Option for seeing courses taught by a teacher in Teacher Details.


def register(bot: TeleBot):
    cancelMarkup = types.InlineKeyboardMarkup()
    cancelMarkup.add(types.InlineKeyboardButton(
        "Cancel", callback_data="cancel"))

    TEACHER_FIELDS = [
        ('name', "the teacher's name"),
        ('email', "email"),
        ('phone_number', "phone (<Optional>)"),
        ('password', "password"),
        ('username', "username"),
        ('birthday', "birthday (YY/MM/DD)"),
        ('about_me', "about me"),
        ('job_title', "job title"),
    ]
    EDITABLE_FIELDS = {
        'name': 2,
        'email': 4,
        'phone_number': 5,
        'password': 3,
        'username': 1,
        'birthday': 8,
        'about_me': 9,
        'job_title': 10
    }

    # Showing details of a Teacher
    @bot.callback_query_handler(func=lambda call: call.data.startswith('teacher_'))
    def show_teacher_details(call):
        teacher_id = call.data.split('_')[1]
        teacher = Teachers.getTeacherById(teacher_id)

        if teacher:
            details = format_teacher_info(teacher)
            markup = create_entity_markup("teacher", teacher_id)

            bot.send_message(call.message.chat.id, details,
                             reply_markup=markup, parse_mode="HTML")
        else:
            bot.send_message(call.message.chat.id, "Teacher not found.")

        bot.answer_callback_query(call.id)

    # Creating a Teacher Flow
    @bot.callback_query_handler(func=lambda call: call.data == 'create_teacher')
    def start_teacher_creation(call):
        msg = bot.send_message(call.message.chat.id,
                               "Please enter following data: (enter any key to start)",
                               reply_markup=cancelMarkup)
        bot.register_next_step_handler(msg, collect_field, {}, 0)
        bot.answer_callback_query(call.id)

    def collect_field(message, data, step):
        # Save previous field
        if step > 0:
            field_name = TEACHER_FIELDS[step - 1][0]
            data[field_name] = message.text

        # Done collecting?
        if step >= len(TEACHER_FIELDS):
            show_confirmation(message, data)
            return

        # Ask next question
        field_name, prompt = TEACHER_FIELDS[step]
        msg = bot.send_message(message.chat.id, f"Now enter {prompt}:",
                               reply_markup=cancelMarkup)
        bot.register_next_step_handler(msg, collect_field, data, step + 1)

    def show_confirmation(message, data):
        summary = "Is this correct? (enter any key to continue or cancel to exit)\n\n" + "\n".join(
            f"{name.replace('_', ' ').title()}: {data[name]}"
            for name, _ in TEACHER_FIELDS
        )
        msg = bot.send_message(message.chat.id, summary,
                               reply_markup=cancelMarkup)
        bot.register_next_step_handler(msg, create_teacher, data)

    def create_teacher(message, data):
        if Teachers.createTeacher(**data):
            bot.send_message(message.chat.id, "✅ Teacher created!",
                             reply_markup=startMarkup())
        else:
            bot.send_message(
                message.chat.id, "❌ Failed to create teacher.", reply_markup=startMarkup())

    # Editing a Teacher Flow
    @bot.callback_query_handler(func=lambda call: call.data.startswith('edit_teacher_'))
    def start_teacher_editing(call):
        teacher_id = call.data.split('_')[2]
        teacher = Teachers.getTeacherById(teacher_id)

        if not teacher:
            bot.send_message(call.message.chat.id, "Teacher not found.")
            bot.answer_callback_query(call.id)
            return

        editMarkup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True)
        for field in list(EDITABLE_FIELDS.keys()) + ['Cancel']:
            editMarkup.add(types.KeyboardButton(field.capitalize()))

        msg = bot.send_message(call.message.chat.id,
                               "Please enter the field you want to edit: ", reply_markup=editMarkup)

        bot.register_next_step_handler(
            msg, process_field_select, teacher)
        bot.answer_callback_query(call.id)

    def process_field_select(message, teacher: tuple):
        field = message.text.lower()
        if field == 'cancel' or field not in EDITABLE_FIELDS:
            msg = "Action cancelled." if field == 'cancel' else "Invalid field. Action cancelled."
            bot.send_message(message.chat.id, msg,
                             reply_markup=startMarkup())
            return

        current_value = teacher[EDITABLE_FIELDS[field]]

        msg = bot.send_message(
            message.chat.id, f"Current value is: {current_value if field != 'password' else '********'}.\n Please enter new value for {field}:", reply_markup=cancelMarkup)
        bot.register_next_step_handler(
            msg, process_value_edit, teacher[0], field, current_value)

    def process_value_edit(message, teacher_id, field, previous_value):
        new_value = message.text

        # Handle cancellation
        if new_value.lower() == 'cancel' or new_value == f"{previous_value}":
            msg = "Action cancelled." if new_value.lower(
            ) == 'cancel' else f"No changes made to {field}."
            bot.send_message(message.chat.id, msg, reply_markup=startMarkup())
            return

        # Update teacher
        if Teachers.updateTeacher(teacher_id, **{field: new_value}):
            bot.send_message(
                message.chat.id, f"✅ Teacher's {field} updated successfully.", reply_markup=startMarkup())
        else:
            bot.send_message(
                message.chat.id, f"❌ Failed to update Teacher's {field}.", reply_markup=startMarkup())

    # Deleting a Teacher
    @bot.callback_query_handler(func=lambda call: call.data.startswith('delete_teacher_'))
    def delete_teacher(call):
        teacher_id = call.data.split('_')[2]
        if (Teachers.deleteTeacher(teacher_id)):
            bot.send_message(call.message.chat.id, "✅ Teacher deleted.",
                             reply_markup=startMarkup())
        else:
            bot.send_message(call.message.chat.id, "❌ Failed to delete Teacher.",
                             reply_markup=startMarkup())
        bot.answer_callback_query(call.id)
