import os
import telebot
import logging
from bot.handlers.init import register_all_handlers

logger = logging.getLogger(__name__)

_bot = None


def get_bot():
    global _bot
    if _bot is None:
        BOT_TOKEN = os.environ.get("BOT_TOKEN")
        _bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
        register_all_handlers(_bot)
        logger.info("Telegram bot initialized.")
    return _bot
