from . import students, teachers


def register_all_callbacks(bot):
    """Register all callback handlers"""
    students.register(bot)
    teachers.register(bot)
