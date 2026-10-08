import os
import asyncio
import threading

from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.environ["BOT_TOKEN"]

app = Flask(__name__)

@app.route("/")
def home():
    return "Ringtonlar bot ishlayapti!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """🌙 Kun ishorasi

O‘zingni boshqalar bilan solishtirishni to‘xtat.

Sen ularning yo‘lini emas, o‘zingga berilgan yo‘lni bosib o‘tyapsan.

Sekin ketayotgan bo‘lsang ham, ortga qaytmayotganing muhim."""

    await update.message.reply_text(text)

async def main():
    bot = Application.builder().token(TOKEN).build()
    bot.add_handler(CommandHandler("start", start))

    await bot.initialize()
    await bot.start()
    await bot.updater.start_polling()

    await asyncio.Event().wait()

def run_flask():
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    asyncio.run(main())
