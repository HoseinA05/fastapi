from . import start, students, teachers, courses, tags, categories, common
from bot.callbacks.init import register_all_callbacks


def register_all_handlers(bot):
    """Register all handlers and callbacks"""
    # Message handlers
    start.register(bot)
    students.register(bot)
    teachers.register(bot)
    courses.register(bot)
    tags.register(bot)
    categories.register(bot)
    common.register(bot)  # Must be last (catch-all)

    # Callback handlers
    register_all_callbacks(bot)
