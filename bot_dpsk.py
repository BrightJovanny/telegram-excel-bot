from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import pandas as pd

# Read buttons from Excel
def get_buttons_from_excel():
    df = pd.read_excel('buttons.xlsx', header=None)
    keyboard = []
    
    for i in range(len(df)):
        row_buttons = []
        for j in range(0, len(df.columns), 2):  # Skip every other column for data
            if pd.notna(df.iloc[i, j]):
                row_buttons.append(
                    InlineKeyboardButton(
                        df.iloc[i, j], 
                        callback_data=df.iloc[i, j+1]
                    )
                )
        keyboard.append(row_buttons)
    
    return InlineKeyboardMarkup(keyboard)

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = get_buttons_from_excel()
    await update.message.reply_text('Choose an option:', reply_markup=keyboard)

# Handle button presses
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # You can add different actions based on callback_data
    await query.edit_message_text(f"Selected: {query.data}")

# Main function
def main():
    application = Application.builder().token("1256084778:AAEAQR4QQM2vRVgDzEjEfxXJ6rDLWK6udng").build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    application.run_polling()

if __name__ == "__main__":
    main()
