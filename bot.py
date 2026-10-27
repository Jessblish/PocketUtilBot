import os
import telebot
import base64
import hashlib
import string
import random

# Fetch token from Railway Environment Variables
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise ValueError("No BOT_TOKEN environment variable found! Please set it in Railway.")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    help_text = (
        "🛠 *PocketUtil Bot*\n\n"
        "Here are your available offline tools:\n"
        "• `/password [length]` - Generate a secure random password (default 12)\n"
        "• `/base64 <text>` - Encode text to Base64\n"
        "• `/decode <text>` - Decode Base64 text\n"
        "• `/hash <text>` - Generate SHA-256 hash\n"
    )
    bot.reply_to(message, help_text, parse_mode="Markdown")

@bot.message_handler(commands=['password'])
def generate_password(message):
    try:
        parts = message.text.split()
        length = int(parts[1]) if len(parts) > 1 else 12
        if length < 4 or length > 128:
            length = 12
        
        chars = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(chars) for _ in range(length))
        bot.reply_to(message, f"🔐 *Generated Password:*\n`{password}`", parse_mode="Markdown")
    except Exception:
        bot.reply_to(message, "Usage: `/password [length]` (e.g., `/password 16`)", parse_mode="Markdown")

@bot.message_handler(commands=['base64'])
def encode_base64(message):
    try:
        text = message.text.replace('/base64', '', 1).strip()
        if not text:
            bot.reply_to(message, "Please provide text to encode. Example: `/base64 Hello World`", parse_mode="Markdown")
            return
        encoded = base64.b64encode(text.encode('utf-8')).decode('utf-8')
        bot.reply_to(message, f"📤 *Base64 Encoded:*\n`{encoded}`", parse_mode="Markdown")
    except Exception:
        bot.reply_to(message, "Error encoding text.")

@bot.message_handler(commands=['decode'])
def decode_base64(message):
    try:
        text = message.text.replace('/decode', '', 1).strip()
        if not text:
            bot.reply_to(message, "Please provide Base64 text to decode. Example: `/decode SGVsbG8gV29ybGQ=`", parse_mode="Markdown")
            return
        decoded = base64.b64decode(text.encode('utf-8')).decode('utf-8')
        bot.reply_to(message, f"📥 *Decoded Text:*\n`{decoded}`", parse_mode="Markdown")
    except Exception:
        bot.reply_to(message, "Invalid Base64 string format.")

@bot.message_handler(commands=['hash'])
def generate_hash(message):
    try:
        text = message.text.replace('/hash', '', 1).strip()
        if not text:
            bot.reply_to(message, "Please provide text to hash. Example: `/hash mypassword`", parse_mode="Markdown")
            return
        hash_result = hashlib.sha256(text.encode('utf-8')).hexdigest()
        bot.reply_to(message, f"#️⃣ *SHA-256 Hash:*\n`{hash_result}`", parse_mode="Markdown")
    except Exception:
        bot.reply_to(message, "Error generating hash.")

if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()
