import logging
import os
import requests
import json
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
KEYWORDS = ["urgent", "refund", "help", "return policy"]

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

async def check_keyword(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    if not message or not message.text:
        return

    text = message.text or message.caption or ""
    if not text:
        return

    lowered = text.lower()
    matched = [k for k in KEYWORDS if k.lower() in lowered]

    logging.info("Checking text: %r | matched=%s", text, matched)

    if matched:
        payload = {"question": message.text}
        response = requests.post("https://ecl1ps0.app.n8n.cloud/webhook/73ab3c5e-5fc5-4b1f-af8d-b7cf2fb767c8", json = payload)
        response.raise_for_status()
        data = response.json()
        await message.reply_text(data.get("answer"))

def main() -> None:
    if not BOT_TOKEN:
        raise ValueError("Set BOT_TOKEN environment variable first.")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_keyword), group=1)

    app.run_polling()

if __name__ == "__main__":
    main()