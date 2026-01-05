from telebot import types, TeleBot
from database.models import Admins
from bot.handlers.start import startMarkup


def register(bot: TeleBot):

    @bot.message_handler(commands=['login'])
    def start_login(message):
        # Check if already authenticated
        if Admins.is_authenticated(message.from_user.id):
            session_info = Admins.get_session_info(message.from_user.id)
            bot.send_message(
                message.chat.id,
                f"✅ You are already logged in!\n\n"
                f"Session expires in: {session_info['time_remaining']}"
            )
            return

        msg = bot.send_message(
            message.chat.id,
            "🔐 Please enter your username:"
        )
        bot.register_next_step_handler(msg, get_password)

    def get_password(message):
        """Get username and ask for password"""
        username = message.text.strip()

        try:
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass

        msg = bot.send_message(
            message.chat.id,
            f"Username: {username}\n\n🔑 Now enter your password:"
        )
        bot.register_next_step_handler(msg, verify_and_login, username)

    def verify_and_login(message, username):
        """Verify credentials and create session"""
        password = message.text.strip()
        telegram_id = message.from_user.id

        try:
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass

        # Attempt login (this creates the session)
        if Admins.login(username, password, telegram_id):
            bot.send_message(
                message.chat.id,
                f"✅ Login successful!\n\n"
                f"Welcome back, {username}!\n"
                f"Session valid for: {Admins.SESSION_TIMEOUT_HOURS} hours\n"
                f"Use /session for info about your session, or /logout to logout.",
                reply_markup=startMarkup()
            )
        else:
            bot.send_message(
                message.chat.id,
                "❌ Invalid credentials or unauthorized Telegram account.\n\n"
                "Please check your username and password.\nContact @HoseinA05 for support."
            )

    @bot.message_handler(commands=['logout'])
    def logout(message):
        """Logout user manually"""

        if not Admins.is_authenticated(message.from_user.id):
            bot.send_message(message.chat.id, "You are not logged in.")
            return

        if Admins.logout(message.from_user.id):
            bot.send_message(
                message.chat.id,
                "✅ You have been logged out successfully.\n\n"
                "Use /login to access admin features again."
            )
        else:
            bot.send_message(
                message.chat.id, "❌ Logout failed. Please try again later.")

    @bot.message_handler(commands=['session'])
    def check_session(message):
        """Check current session status"""
        session_info = Admins.get_session_info(message.from_user.id)

        if not session_info:
            bot.send_message(
                message.chat.id, "❌ You don't have an admin account.")
            return

        if session_info['is_active']:
            bot.send_message(
                message.chat.id,
                f"✅ Active Session\n\n"
                f"Username: {session_info['username']}\n"
                f"Last Login: {session_info['last_login']}\n"
                f"Time Remaining: {session_info['time_remaining']}"
            )
        else:
            bot.send_message(
                message.chat.id,
                f"⏱️ Session Expired\n\n"
                f"Username: {session_info['username']}\n"
                f"Please use /login to continue."
            )
