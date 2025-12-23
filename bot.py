import os

_bot = None

def get_bot():
    global _bot
    if _bot is None:
        import telebot
        BOT_TOKEN = os.environ.get("BOT_TOKEN")
        _bot = telebot.TeleBot(BOT_TOKEN)
        
        # Register handlers
        @_bot.message_handler(commands=["start"])
        def start(message):
            _bot.reply_to(message, "Welcome!")
    
    return _bot