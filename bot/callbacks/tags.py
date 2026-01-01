from telebot import types, TeleBot
from database.models import Tags
from bot.handlers.start import startMarkup
from bot.utils.crud_helpers import create_entity_markup

# TODO: Add Option for showing courses with specific tags.


def register(bot: TeleBot):
    cancelMarkup = types.InlineKeyboardMarkup()
    cancelMarkup.add(types.InlineKeyboardButton(
        "Cancel", callback_data="cancel"))

    TAG_FIELDS = [
        ('name', "the tag's name"),
        ('slug', "The slug for tag")
    ]
    EDITABLE_FIELDS = {
        'name': 1,
        'slug': 2
    }

    # Showing details of a Tag
    @bot.callback_query_handler(func=lambda call: call.data.startswith('tag_'))
    def show_teacher_details(call):
        tag_id = call.data.split('_')[1]
        tag = Tags.getTagById(tag_id)

        if tag:
            details = f"""
            <b>🔖 Tag Profile</b>

            <b>Name:</b> {tag[1]}
            <b>slug:</b> {tag[2]}
            """
            details.strip()
            markup = create_entity_markup("tag", tag_id)

            bot.send_message(call.message.chat.id, details,
                             reply_markup=markup, parse_mode="HTML")
        else:
            bot.send_message(call.message.chat.id, "Tag not found.")

        bot.answer_callback_query(call.id)

    # Creating a Tag Flow
    @bot.callback_query_handler(func=lambda call: call.data == 'create_tag')
    def start_tag_creation(call):
        msg = bot.send_message(call.message.chat.id,
                               "Please enter following data: (enter any key to start)",
                               reply_markup=cancelMarkup)
        bot.register_next_step_handler(msg, collect_field, {}, 0)
        bot.answer_callback_query(call.id)

    def collect_field(message, data, step):
        # Save previous field
        if step > 0:
            field_name = TAG_FIELDS[step - 1][0]
            data[field_name] = message.text

        # Done collecting?
        if step >= len(TAG_FIELDS):
            show_confirmation(message, data)
            return

        # Ask next question
        field_name, prompt = TAG_FIELDS[step]
        msg = bot.send_message(message.chat.id, f"Now enter {prompt}:",
                               reply_markup=cancelMarkup)
        bot.register_next_step_handler(msg, collect_field, data, step + 1)

    def show_confirmation(message, data):
        summary = "Is this correct? (enter any key to continue or cancel to exit)\n\n" + "\n".join(
            f"{name.replace('_', ' ').title()}: {data[name]}"
            for name, _ in TAG_FIELDS
        )
        msg = bot.send_message(message.chat.id, summary,
                               reply_markup=cancelMarkup)
        bot.register_next_step_handler(msg, create_tag, data)

    def create_tag(message, data):
        if Tags.createTag(**data):
            bot.send_message(message.chat.id, "✅ Tag created!",
                             reply_markup=startMarkup())
        else:
            bot.send_message(
                message.chat.id, "❌ Failed to create tag.", reply_markup=startMarkup())

    # Editing a Tag Flow

    @bot.callback_query_handler(func=lambda call: call.data.startswith('edit_tag_'))
    def start_tag_editing(call):
        tag_id = call.data.split('_')[2]
        tag = Tags.getTagById(tag_id)

        if not tag:
            bot.send_message(call.message.chat.id, "Tag not found.")
            bot.answer_callback_query(call.id)
            return

        editMarkup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True)
        for field in list(EDITABLE_FIELDS.keys()) + ['Cancel']:
            editMarkup.add(types.KeyboardButton(field.capitalize()))

        msg = bot.send_message(call.message.chat.id,
                               "Please enter the field you want to edit: ", reply_markup=editMarkup)

        bot.register_next_step_handler(
            msg, process_field_select, tag)
        bot.answer_callback_query(call.id)

    def process_field_select(message, tag: tuple):
        field = message.text.lower()
        if field == 'cancel' or field not in EDITABLE_FIELDS:
            msg = "Action cancelled." if field == 'cancel' else "Invalid field. Action cancelled."
            bot.send_message(message.chat.id, msg,
                             reply_markup=startMarkup())
            return

        current_value = tag[EDITABLE_FIELDS[field]]

        msg = bot.send_message(
            message.chat.id, f"Current value is: {current_value}.\n Please enter new value for {field}:", reply_markup=cancelMarkup)
        bot.register_next_step_handler(
            msg, process_value_edit, tag[0], field, current_value)

    def process_value_edit(message, tag_id, field, previous_value):
        new_value = message.text

        # Handle cancellation
        if new_value.lower() == 'cancel' or new_value == f"{previous_value}":
            msg = "Action cancelled." if new_value.lower(
            ) == 'cancel' else f"No changes made to {field}."
            bot.send_message(message.chat.id, msg, reply_markup=startMarkup())
            return

        # Update teacher
        if Tags.updateTag(tag_id, **{field: new_value}):
            bot.send_message(
                message.chat.id, f"✅ Tag's {field} updated successfully.", reply_markup=startMarkup())
        else:
            bot.send_message(
                message.chat.id, f"❌ Failed to update Tag's {field}.", reply_markup=startMarkup())

    # Deleting a Teacher
    @bot.callback_query_handler(func=lambda call: call.data.startswith('delete_tag_'))
    def delete_tag(call):
        tag_id = call.data.split('_')[2]
        if (Tags.deleteTag(tag_id)):
            bot.send_message(call.message.chat.id, "✅ Tag deleted.",
                             reply_markup=startMarkup())
        else:
            bot.send_message(call.message.chat.id, "❌ Failed to delete Tag.",
                             reply_markup=startMarkup())
        bot.answer_callback_query(call.id)
