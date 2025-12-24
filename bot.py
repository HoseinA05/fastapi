import os

_bot = None

def get_bot():
    global _bot
    if _bot is None:
        import telebot
        BOT_TOKEN = os.environ.get("BOT_TOKEN")
        _bot = telebot.TeleBot(BOT_TOKEN, threaded=False)  # threaded=False for serverless
        
        # Register handlers
        @_bot.message_handler(commands=["start"])
        def start(message):
            _bot.reply_to(message, "Welcome!")
        
        # Add a handler for all other messages
        @_bot.message_handler(func=lambda message: True)
        def echo_all(message):
            _bot.reply_to(message, f"You said: {message.text}")
    
    return _bot