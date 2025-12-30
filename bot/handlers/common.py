def register(bot):
    @bot.message_handler(func=lambda message: True)
    def handle_unknown(message):
        bot.reply_to(message, f"You said: {message.text}")
