import os
import requests
from bot import get_bot
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")

def ensure_no_webhook():
    """Remove webhook before starting polling"""
    response = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook"
    )
    if response.json()['ok']:
        print("✅ Webhook removed, starting polling...")
        return True
    
    print("⚠️  Warning: Could not remove webhook")
    return False
  

if __name__ == "__main__":
    if ensure_no_webhook():
        bot = get_bot()
        print("🤖 Bot is polling locally...")
        bot.polling(non_stop=True)