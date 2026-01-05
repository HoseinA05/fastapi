from telebot import types, TeleBot
from database.models import Students, Admins
from bot.utils.formatters import format_student_info
from bot.utils.crud_helpers import create_entity_markup
from bot.handlers.start import startMarkup


def register(bot: TeleBot):
    cancelMarkup = types.InlineKeyboardMarkup()
    cancelMarkup.add(types.InlineKeyboardButton(
        "Cancel", callback_data="cancel"))

    STUDENT_FIELDS = [
        ('name', "the student's name"),
        ('email', "email"),
        ('phone_number', "phone (<Optional>)"),
        ('password', "password"),
        ('username', "username"),
        ('birthday', "birthday (YY/MM/DD)"),
    ]
    EDITABLE_FIELDS = {
        'name': 2,
        'email': 4,
        'phone_number': 5,
        'password': 3,
        'username': 1,
        'birthday': 8,
    }

    # Showing details of a Student
    @bot.callback_query_handler(func=lambda call: call.data.startswith('student_'))
    def show_student_details(call):
        if not Admins.is_authenticated(call.from_user.id):
            bot.answer_callback_query(call.id, "⛔ Unauthorized access!")
            bot.send_message(call.message.chat.id, "Please /login first.")
            return

        student_id = call.data.split('_')[1]
        student = Students.getStudentById(student_id)

        if student:
            details = format_student_info(student)
            markup = create_entity_markup("student", student_id, True)

            bot.send_message(call.message.chat.id, details,
                             reply_markup=markup, parse_mode="HTML")
        else:
            bot.send_message(call.message.chat.id, "Student not found.")

        bot.answer_callback_query(call.id)

    # Creating a Student Flow
    @bot.callback_query_handler(func=lambda call: call.data == 'create_student')
    def create_student(call):
        if not Admins.is_authenticated(call.from_user.id):
            bot.answer_callback_query(call.id, "⛔ Unauthorized access!")
            bot.send_message(call.message.chat.id, "Please /login first.")
            return

        msg = bot.send_message(call.message.chat.id,
                               "Please enter following data: (enter any key to start)",
                               reply_markup=cancelMarkup)
        bot.register_next_step_handler(msg, collect_field, {}, 0)
        bot.answer_callback_query(call.id)

    def collect_field(message, data, step):
        # Save previous field
        if step > 0:
            field_name = STUDENT_FIELDS[step - 1][0]
            data[field_name] = message.text

        # Done collecting?
        if step >= len(STUDENT_FIELDS):
            show_confirmation(message, data)
            return

        # Ask next question
        field_name, prompt = STUDENT_FIELDS[step]
        msg = bot.send_message(message.chat.id, f"Now enter {prompt}:",
                               reply_markup=cancelMarkup)
        bot.register_next_step_handler(msg, collect_field, data, step + 1)

    def show_confirmation(message, data):
        summary = "Is this correct? (enter any key to continue or cancel to exit)\n\n" + "\n".join(
            f"{name.replace('_', ' ').title()}: {data[name]}"
            for name, _ in STUDENT_FIELDS
        )
        msg = bot.send_message(message.chat.id, summary,
                               reply_markup=cancelMarkup)
        bot.register_next_step_handler(msg, create_student, data)

    def create_student(message, data):
        if Students.createStudent(**data):
            bot.send_message(message.chat.id, "✅ Student created!",
                             reply_markup=startMarkup())
        else:
            bot.send_message(
                message.chat.id, "❌ Failed to create student.", reply_markup=startMarkup())

    # Editing a Student Flow
    @bot.callback_query_handler(func=lambda call: call.data.startswith('edit_student_'))
    def start_student_editing(call):
        if not Admins.is_authenticated(call.from_user.id):
            bot.answer_callback_query(call.id, "⛔ Unauthorized access!")
            bot.send_message(call.message.chat.id, "Please /login first.")
            return

        student_id = call.data.split('_')[2]
        student = Students.getStudentById(student_id)

        if not student:
            bot.send_message(call.message.chat.id, "Student not found.")
            bot.answer_callback_query(call.id)
            return

        editMarkup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True)
        for field in list(EDITABLE_FIELDS.keys()) + ['Cancel']:
            editMarkup.add(types.KeyboardButton(field.capitalize()))

        msg = bot.send_message(call.message.chat.id,
                               "Please enter the field you want to edit: ", reply_markup=editMarkup)

        bot.register_next_step_handler(
            msg, process_field_select, student)
        bot.answer_callback_query(call.id)

    def process_field_select(message, student: tuple):
        field = message.text.lower()
        if field == 'cancel' or field not in EDITABLE_FIELDS:
            msg = "Action cancelled." if field == 'cancel' else "Invalid field. Action cancelled."
            bot.send_message(message.chat.id, msg,
                             reply_markup=startMarkup())
            return

        current_value = student[EDITABLE_FIELDS[field]]

        msg = bot.send_message(
            message.chat.id, f"Current value is: {current_value if field != 'password' else '********'}.\n Please enter new value for {field}:", reply_markup=cancelMarkup)
        bot.register_next_step_handler(
            msg, process_value_edit, student[0], field, current_value)

    def process_value_edit(message, student_id, field, previous_value):
        new_value = message.text

        # Handle cancellation
        if new_value.lower() == 'cancel' or new_value == f"{previous_value}":
            msg = "Action cancelled." if new_value.lower(
            ) == 'cancel' else f"No changes made to {field}."
            bot.send_message(message.chat.id, msg, reply_markup=startMarkup())
            return

        # Update student
        if Students.updateStudent(student_id, **{field: new_value}):
            bot.send_message(
                message.chat.id, f"✅ Student's {field} updated successfully.", reply_markup=startMarkup())
        else:
            bot.send_message(
                message.chat.id, f"❌ Failed to update Student's {field}.", reply_markup=startMarkup())

    # Deleting a Teacher
    @bot.callback_query_handler(func=lambda call: call.data.startswith('delete_student_'))
    def delete_student(call):
        if not Admins.is_authenticated(call.from_user.id):
            bot.answer_callback_query(call.id, "⛔ Unauthorized access!")
            bot.send_message(call.message.chat.id, "Please /login first.")
            return

        student_id = call.data.split('_')[2]
        if (Students.deleteStudent(student_id)):
            bot.send_message(call.message.chat.id, "✅ Student deleted.",
                             reply_markup=startMarkup())
        else:
            bot.send_message(call.message.chat.id, "❌ Failed to delete Student.",
                             reply_markup=startMarkup())
        bot.answer_callback_query(call.id)
