import os
import logging
from database.models import Students 
from telebot import types
from datetime import datetime

logger = logging.getLogger(__name__)

authenticated_users = {2032936226}
_bot = None

def get_bot():
    global _bot
    if _bot is None:
        import telebot
        BOT_TOKEN = os.environ.get("BOT_TOKEN")
        _bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
        
        @_bot.message_handler(commands=["start"])
        def start(message):
            if message.from_user.id in authenticated_users:
                _bot.reply_to(message, "authorized user! Welcome. Use /getstudents to fetch from database.")
                return
            _bot.reply_to(message, "Welcome! Use /getstudents to fetch from database.")

        @_bot.message_handler(commands=["getstudents"])
        def get_data(message):
            try:
                data = Students.getAllStudents()
                if data:

                    markup = types.InlineKeyboardMarkup(row_width=2)
                    for row in data:
                        btn = types.InlineKeyboardButton(f"{row[0]}: @{row[1]}", callback_data=f"student_{row[0]}")
                        markup.add(btn)

                    _bot.send_message(message.chat.id, "Here is the data:", reply_markup=markup)
                else:
                    _bot.reply_to(message, "No data found.")
                    return                    
            except Exception as e:
                logger.error(f"Error in getdata handler: {e}")
                _bot.reply_to(message, "Sorry, an error occurred.")
        
        # Single handler for all student selections
        @_bot.callback_query_handler(func=lambda call: call.data.startswith('student_'))
        def show_student_details(call):
            student_id = call.data.split('_')[1]
            student = Students.getStudentById(student_id)

            if student:
                details = format_student_info(student)
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="back_to_students"))
                _bot.send_message(call.message.chat.id, details, reply_markup=markup, parse_mode="HTML")
            else:
                _bot.send_message(call.message.chat.id, "Student not found.")

        def format_student_info(student):
            """
            Format student data into a nice message
            student is a tuple: (id, username, created_at, email, phone_number, last_seen, is_verified, birthday)
            """
            print(student);
            id, username, created_at, email, phone_number, last_seen, is_verfied, birthday = student
            
            verified_status = "✅ Verified" if is_verfied else "❌ Not Verified"
            
            # Format dates nicely
            created_date = format_date(created_at)
            last_seen_date = format_date(last_seen)
            
            # Calculate age from birthday
            age = calculate_age(birthday)
            
            details = f"""
            <b>👤 Student Profile</b>

            <b>Username:</b> {username}
            <b>Email:</b> {email}
            <b>Phone:</b> {phone_number}
            <b>Birthday:</b> {birthday} (Age: {age})
            <b>Account Status:</b> {verified_status}

            <b>📅 Account Info</b>
            <b>Joined:</b> {created_date}
            <b>Last Seen:</b> {last_seen_date}
            <b>ID:</b> <code>{id}</code>
            """
            return details.strip()

        def format_date(date_string):
            """Convert database date to readable format"""
            if not date_string:
                return "N/A"
            
            try:
                # If date_string is already a datetime object
                if isinstance(date_string, datetime):
                    return date_string.strftime("%d %b %Y, %H:%M")
                
                # If it's a string, parse it first
                date_obj = datetime.strptime(str(date_string), "%Y-%m-%d %H:%M:%S")
                return date_obj.strftime("%d %b %Y, %H:%M")
            except:
                return str(date_string)

        def calculate_age(birthday_string):
            """Calculate age from birthday"""
            if not birthday_string:
                return "N/A"
            
            try:
                birth_date = datetime.strptime(str(birthday_string), "%Y-%m-%d").date()
                today = datetime.now().date()
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                return age
            except:
                return "N/A"
    

        @_bot.message_handler(commands=["test"])
        def test_handler(message):
            markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
            btn1 = types.KeyboardButton("Option 1")
            btn2 = types.KeyboardButton("Option 2")
            markup.add(btn1, btn2)
            _bot.reply_to(message, "Test command received!", reply_markup=markup)

        @_bot.message_handler(func=lambda message: message.text in ["Option 1", "Option 2"])
        def handle_test_options(message):
            option = message.text
            _bot.send_message(message.chat.id, f"You selected: {option}")

        @_bot.message_handler(func=lambda message: True)
        def handle_student_selection(message):
            chat_id = message.chat.id
            selected_text = message.text

            _bot.reply_to(message, f"You said: {message.text}")
        
    return _bot