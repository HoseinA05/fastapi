from . import start, students, teachers, courses, tags, categories, common, login
from bot.callbacks.init import register_all_callbacks
from telebot import types


def register_all_handlers(bot):
    """Register all handlers and callbacks"""
    # Set bot commands
    commands = [
        types.BotCommand(command="start", description="Start the bot"),
        types.BotCommand(command="login", description="Login to your account"),
        types.BotCommand(command="logout",
                         description="Logout of your account"),
        types.BotCommand(command="session",
                         description="Info about your session"),
    ]

    bot.set_my_commands(commands)

    # Message handlers
    start.register(bot)
    login.register(bot)
    students.register(bot)
    teachers.register(bot)
    courses.register(bot)
    tags.register(bot)
    categories.register(bot)
    common.register(bot)  # Must be last (catch-all)

    # Callback handlers
    register_all_callbacks(bot)
