from telebot import types, TeleBot
from database.models import Categories, Admins
from bot.handlers.start import startMarkup
from bot.utils.crud_helpers import create_entity_markup

# TODO: Add Option for showing parent categories when creating a new category.


def register(bot: TeleBot):
    cancelMarkup = types.InlineKeyboardMarkup()
    cancelMarkup.add(types.InlineKeyboardButton(
        "Cancel", callback_data="cancel"))

    CATEGORY_FIELDS = [
        ('name', "the category's name"),
        ('description', "The description for category (<Optional>) ('s' to skip)"),
        ('parent_id', "The parent category id (<Optional>) ('s' to skip))")
    ]
    EDITABLE_FIELDS = {
        'name': 1,
        'description': 2,
        'parent_id': 3
    }

    # Showing details of a Category
    @bot.callback_query_handler(func=lambda call: call.data.startswith('category_'))
    def show_category_details(call):
        category_id = call.data.split('_')[1]
        category = Categories.getCategoryById(category_id)

        if category:
            details = f"""
            <b>🔖 Category Profile</b>

            <b>Name:</b> {category[1]}
            <b>Parent Category:</b> {category[3]}
            <b>Description:</b> \n{category[2]}
            """
            details.strip()
            markup = create_entity_markup("category", category_id, True)
            markup.add(types.InlineKeyboardButton("📁 Show Top Courses",
                       callback_data=f"categoryCourses_{category_id}"))

            bot.send_message(call.message.chat.id, details,
                             reply_markup=markup, parse_mode="HTML")
        else:
            bot.send_message(call.message.chat.id, "Category not found.")

        bot.answer_callback_query(call.id)

    # Creating a Category Flow
    @bot.callback_query_handler(func=lambda call: call.data == 'create_category')
    def start_category_creation(call):
        msg = bot.send_message(call.message.chat.id,
                               "Please enter following data: (enter any key to start)",
                               reply_markup=cancelMarkup)
        bot.register_next_step_handler(msg, collect_field, {}, 0)
        bot.answer_callback_query(call.id)

    def collect_field(message, data, step):
        # Save previous field
        if step > 0:
            field_name = CATEGORY_FIELDS[step - 1][0]
            data[field_name] = None if (
                (field_name in ['description', 'parent_id']) and message.text == 's') else message.text

        # Done collecting?
        if step >= len(CATEGORY_FIELDS):
            show_confirmation(message, data)
            return

        # Ask next question
        field_name, prompt = CATEGORY_FIELDS[step]
        msg = bot.send_message(message.chat.id, f"Now enter {prompt}:",
                               reply_markup=cancelMarkup)
        bot.register_next_step_handler(msg, collect_field, data, step + 1)

    def show_confirmation(message, data):
        summary = "Is this correct? (enter any key to continue or cancel to exit)\n\n" + "\n".join(
            f"{name.replace('_', ' ').title()}: {data[name]}"
            for name, _ in CATEGORY_FIELDS
        )
        msg = bot.send_message(message.chat.id, summary,
                               reply_markup=cancelMarkup)
        bot.register_next_step_handler(msg, create_category, data)

    def create_category(message, data):
        if Categories.createCategory(**data):
            bot.send_message(message.chat.id, "✅ Category created!",
                             reply_markup=startMarkup())
        else:
            bot.send_message(
                message.chat.id, "❌ Failed to create category.", reply_markup=startMarkup())

    # Editing a Category Flow
    @bot.callback_query_handler(func=lambda call: call.data.startswith('edit_category_'))
    def start_category_editing(call):
        if not Admins.is_authenticated(call.from_user.id):
            bot.answer_callback_query(call.id, "⛔ Unauthorized access!")
            bot.send_message(call.message.chat.id, "Please /login first.")
            return

        category_id = call.data.split('_')[2]
        category = Categories.getCategoryById(category_id)

        if not category:
            bot.send_message(call.message.chat.id, "Category not found.")
            bot.answer_callback_query(call.id)
            return

        editMarkup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True)
        for field in list(EDITABLE_FIELDS.keys()) + ['Cancel']:
            editMarkup.add(types.KeyboardButton(field.capitalize()))

        msg = bot.send_message(call.message.chat.id,
                               "Please enter the field you want to edit: ", reply_markup=editMarkup)

        bot.register_next_step_handler(
            msg, process_field_select, category)
        bot.answer_callback_query(call.id)

    def process_field_select(message, category: tuple):
        field = message.text.lower()
        if field == 'cancel' or field not in EDITABLE_FIELDS:
            msg = "Action cancelled." if field == 'cancel' else "Invalid field. Action cancelled."
            bot.send_message(message.chat.id, msg,
                             reply_markup=startMarkup())
            return

        current_value = category[EDITABLE_FIELDS[field]]

        msg = bot.send_message(
            message.chat.id, f"Current value is: {current_value}.\n Please enter new value for {field}:", reply_markup=cancelMarkup)
        bot.register_next_step_handler(
            msg, process_value_edit, category[0], field, current_value)

    def process_value_edit(message, category_id, field, previous_value):
        new_value = message.text

        # Handle cancellation
        if new_value.lower() == 'cancel' or new_value == f"{previous_value}":
            msg = "Action cancelled." if new_value.lower(
            ) == 'cancel' else f"No changes made to {field}."
            bot.send_message(message.chat.id, msg, reply_markup=startMarkup())
            return

        # Update Category
        if Categories.updateCategory(category_id, **{field: new_value}):
            bot.send_message(
                message.chat.id, f"✅ Category's {field} updated successfully.", reply_markup=startMarkup())
        else:
            bot.send_message(
                message.chat.id, f"❌ Failed to update Category's {field}.", reply_markup=startMarkup())

    # Deleting a Category
    @bot.callback_query_handler(func=lambda call: call.data.startswith('delete_category_'))
    def delete_category(call):
        if not Admins.is_authenticated(call.from_user.id):
            bot.answer_callback_query(call.id, "⛔ Unauthorized access!")
            bot.send_message(call.message.chat.id, "Please /login first.")
            return

        category_id = call.data.split('_')[2]
        if (Categories.deleteCategory(category_id)):
            bot.send_message(call.message.chat.id, "✅ Category deleted.",
                             reply_markup=startMarkup())
        else:
            bot.send_message(call.message.chat.id, "❌ Failed to delete Category.",
                             reply_markup=startMarkup())
        bot.answer_callback_query(call.id)

    # Show Top Courses in a Category
    @bot.callback_query_handler(func=lambda call: call.data.startswith('categoryCourses_'))
    def category_courses(call):
        category_id = call.data.split('_')[1]
        courses = Categories.getTopCoursesByCategory(category_id)

        markup = types.InlineKeyboardMarkup()
        if courses:
            for course in courses:
                markup.add(types.InlineKeyboardButton(
                    course[1], callback_data=f"course_{course[0]}"))
            bot.send_message(
                call.message.chat.id, "📚 Top Courses in this Category:", reply_markup=markup)
        else:
            bot.send_message(
                call.message.chat.id, "There are no courses in this category.", reply_markup=markup)

        bot.answer_callback_query(call.id)
