import os
import pandas as pd
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Get token from environment variable
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not TOKEN:
    raise ValueError("No TELEGRAM_BOT_TOKEN found in environment variables")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Your bot is working!')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Your message handling logic here
    text = update.message.text
    await update.message.reply_text(f'You said: {text}')

def main():
    # Create application
    application = Application.builder().token(TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    # Start polling
    print("Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
