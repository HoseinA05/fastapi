from telebot import types


def create_entity_markup(entity_name, enitity_id, is_auth_needed=False):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(
        f"✏️ Edit {entity_name} " + ("🔒" if is_auth_needed else ""), callback_data=f"edit_{entity_name}_{enitity_id}"))
    markup.add(types.InlineKeyboardButton(
        f"🗑️ Delete {entity_name}" + ("🔒" if is_auth_needed else ""), callback_data=f"delete_{entity_name}_{enitity_id}"))

    return markup
