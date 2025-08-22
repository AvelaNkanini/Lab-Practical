#!/usr/bin/env python3

from dotenv import load_dotenv
import os
import logging
import spacy
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)

from nlp_utils import get_bot_response  # Keep your utils import

# Load environment variables
load_dotenv()

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Define conversation states
CHAT = range(1)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Hello! I am the University Clinic Assistant 🤖.\n"
        "You can ask me about opening hours, bookings, emergencies, or contact info.\n"
        "Type something to start chatting."
    )
    return CHAT

# Handle chat messages
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text
    # Process input with SpaCy (optional for NLP)
    doc = nlp(user_input.lower())
    # Use your existing bot response logic
    response = get_bot_response(user_input)
    await update.message.reply_text(response)
    return CHAT

# Cancel command
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Conversation ended. Type /start to talk again."
    )
    return ConversationHandler.END

def main():
    # Get token from environment
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("Please set TELEGRAM_BOT_TOKEN in your .env file")

    # Initialize bot application
    app = Application.builder().token(token).build()

    # Conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHAT: [MessageHandler(filters.TEXT & ~filters.COMMAND, chat)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Add handlers
    app.add_handler(conv_handler)

    # Run bot
    app.run_polling()

if __name__ == "__main__":
    main()
