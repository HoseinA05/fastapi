from telebot import types, TeleBot
from database.models import Teachers
from bot.utils.formatters import format_teacher_info
from bot.handlers.start import startMarkup


def register(bot: TeleBot):
    cancelMarkup = types.InlineKeyboardMarkup()
    cancelMarkup.add(types.InlineKeyboardButton(
        "Cancel", callback_data="cancel"))

    # Showing details of a Teacher
    @bot.callback_query_handler(func=lambda call: call.data.startswith('teacher_'))
    def show_teacher_details(call):
        teacher_id = call.data.split('_')[1]
        teacher = Teachers.getTeachertById(teacher_id)

        if teacher:
            details = format_teacher_info(teacher)
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Edit Teacher",
                       callback_data=f"edit_teacher_{teacher_id}", switch_inline_query_current_chat="A default name for the teacher..."))
            bot.send_message(call.message.chat.id, details,
                             reply_markup=markup, parse_mode="HTML")
        else:
            bot.send_message(call.message.chat.id, "Teacher not found.")

        bot.answer_callback_query(call.id)

    # Creating a Teacher Flow
    @bot.callback_query_handler(func=lambda call: call.data == 'create_teacher')
    def start_teacher_creation(call):
        msg = bot.send_message(call.message.chat.id,
                               "Please enter the teacher's name:", reply_markup=cancelMarkup)
        bot.register_next_step_handler(
            msg, process_name_step)
        bot.answer_callback_query(call.id)

    def process_name_step(message):
        name = message.text
        msg = bot.send_message(
            message.chat.id, f"Name: {name}\n\nNow enter email:", reply_markup=cancelMarkup)
        bot.register_next_step_handler(msg, process_email_step, name)

    def process_email_step(message, name):
        email = message.text
        msg = bot.send_message(
            message.chat.id, f"Email: {email}\n\nNow enter phone: (<Optional>)", reply_markup=cancelMarkup)
        bot.register_next_step_handler(msg, process_phone_step, name, email)

    def process_phone_step(message, name, email):
        phone = message.text
        msg = bot.send_message(
            message.chat.id, f"Phone: {phone}\n\nNow enter password: ", reply_markup=cancelMarkup)
        bot.register_next_step_handler(
            msg, process_password_step, name, email, phone)

    def process_password_step(message, name, email, phone):
        password = message.text
        msg = bot.send_message(
            message.chat.id, f"password: {password}\n\nNow enter username:", reply_markup=cancelMarkup)
        bot.register_next_step_handler(
            msg, process_username_step, name, email, phone, password)

    def process_username_step(message, name, email, phone, password):
        username = message.text
        msg = bot.send_message(
            message.chat.id, f"username: {username}\n\nNow enter birthday: (YY/MM/DD)", reply_markup=cancelMarkup)
        bot.register_next_step_handler(
            msg, process_birthday_step, name, email, phone, password, username)

    def process_birthday_step(message, name, email, phone, password, username):
        birthday = message.text
        msg = bot.send_message(
            message.chat.id, f"birthday: {birthday}\n\nNow enter about me: ", reply_markup=cancelMarkup)
        bot.register_next_step_handler(
            msg, process_aboutme_step, name, email, phone, password, username, birthday)

    def process_aboutme_step(message, name, email, phone, password, username, birthday):
        about_me = message.text
        msg = bot.send_message(
            message.chat.id, f"about me: {about_me}\n\nNow enter job title: ", reply_markup=cancelMarkup)
        bot.register_next_step_handler(
            msg, process_jobtitle_step, name, email, phone, password, username, birthday, about_me)

    def process_jobtitle_step(message, name, email, phone, password, username, birthday, about_me):
        job_title = message.text
        msg = bot.send_message(message.chat.id, "is this correct? (enter any key) (Use Cancel to Stop creating)\n"
                               f"Name: {name}\n"
                               f"Email: {email}\n"
                               f"Phone: {phone}\n"
                               f"Password: {password}\n"
                               f"Birthday: {birthday}\n"
                               f"About Me: {about_me}\n"
                               f"Job Title: {job_title}",
                               reply_markup=cancelMarkup)

        bot.register_next_step_handler(
            msg, confirm_teacher_creation, name, email, phone, password, username, birthday, about_me, job_title)

    def confirm_teacher_creation(message, name, email, phone, password, username, birthday, about_me, job_title):
        if (Teachers.createTeacher(name=name, email=email, phone_number=phone,
                                   password=password, username=username, birthday=birthday,
                                   about_me=about_me, job_title=job_title)):
            bot.send_message(message.chat.id, "✅ Teacher created!")
        else:
            bot.send_message(message.chat.id, "❌ Failed to create teacher.")

    @bot.callback_query_handler(func=lambda call: call.data == 'cancel')
    def cancel_action(call):
        bot.clear_step_handler(call.message)
        bot.send_message(call.message.chat.id, "Action cancelled.")
        bot.answer_callback_query(call.id)

    # Editing a Teacher Flow
    @bot.callback_query_handler(func=lambda call: call.data.startswith('edit_teacher_'))
    def start_teacher_editing(call):
        teacher_id = call.data.split('_')[2]
        teacher = Teachers.getTeachertById(teacher_id)

        editMarkup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True)

        for field in ['name', 'email', 'phone_number', 'password', 'username', 'birthday', 'about_me', 'job_title', 'Cancel']:
            editMarkup.add(types.KeyboardButton(field.capitalize()))

        if teacher:
            msg = bot.send_message(call.message.chat.id,
                                   "Please enter the field you want to edit: ", reply_markup=editMarkup)

            bot.register_next_step_handler(
                msg, process_field_select_step, teacher)
        else:
            bot.send_message(call.message.chat.id, "Teacher not found.")

        bot.answer_callback_query(call.id)

    def process_field_select_step(message, teacher: tuple):
        field = message.text.lower()
        if field == 'cancel':
            bot.send_message(message.chat.id, "Action cancelled.")
            return

        fields = ['id', 'username', 'name', 'created_at', 'email', 'phone_number', 'last_seen', 'is_verfied',
                  'birthday', 'about_me', 'job_title']
        fields_index = {field: i for i, field in enumerate(fields)}

        if field in fields:
            previous_value = teacher[fields_index[field]]

            markup = types.ReplyKeyboardMarkup(
                resize_keyboard=True, one_time_keyboard=True, row_width=1)
            markup.add(types.KeyboardButton(
                f"{previous_value} (current)"), types.KeyboardButton("Cancel"))

            msg = bot.send_message(
                message.chat.id, f"Please enter new value for {field}:", reply_markup=markup)
            bot.register_next_step_handler(
                msg, process_value_edit_step, teacher[fields_index["id"]], field, previous_value)
        else:
            bot.send_message(
                message.chat.id, "Invalid field. Action cancelled.")

    def process_value_edit_step(message, teacher_id, field, previous_value):
        new_value = message.text
        if (new_value.lower() == 'cancel'):
            bot.send_message(message.chat.id, "Action cancelled.",
                             reply_markup=startMarkup())
            return

        if (new_value == f"{previous_value} (current)"):
            bot.send_message(
                message.chat.id, f"No changes made to Teacher's {field}.", reply_markup=startMarkup())
            return

        if (Teachers.updateTeacher(teacher_id, **{field: new_value})):
            bot.send_message(
                message.chat.id, f"✅ Teacher's {field} updated successfully.", reply_markup=startMarkup())
        else:
            bot.send_message(
                message.chat.id, f"❌ Failed to update Teacher's {field}.", reply_markup=startMarkup())
