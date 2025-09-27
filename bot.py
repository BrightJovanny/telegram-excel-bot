import os
import logging
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Create Flask app for port binding
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Telegram Bot is running on Render!"

@app.route('/health')
def health():
    return "✅ OK", 200

# Telegram bot functions
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Your bot is working on Render!')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f'You said: {text}')

def run_flask():
    """Run Flask app on the port Render provides"""
    port = int(os.environ.get('PORT', 10000))
    logger.info(f"Starting Flask server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)

def run_bot():
    """Run Telegram bot"""
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not TOKEN:
        logger.error("❌ No TELEGRAM_BOT_TOKEN found!")
        return
    
    try:
        logger.info("🤖 Starting Telegram bot...")
        application = Application.builder().token(TOKEN).build()
        
        # Add handlers
        application.add_handler(CommandHandler('start', start_command))
        
        # Start polling
        logger.info("✅ Bot started successfully!")
        application.run_polling(drop_pending_updates=True)
    except Exception as e:
        logger.error(f"❌ Bot error: {e}")

def main():
    logger.info("🚀 Starting application...")
    
    # Start Flask server in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Start the bot in the main thread
    run_bot()

if __name__ == '__main__':
    main()
