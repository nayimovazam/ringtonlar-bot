import os
import asyncio
import threading

from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler

TOKEN = os.environ["BOT_TOKEN"]
WEBHOOK_URL = os.environ["WEBHOOK_URL"]

app = Flask(__name__)

bot_app = Application.builder().token(TOKEN).build()


async def start(update: Update, context):
    text = """🌙 Kun ishorasi

O‘zingni boshqalar bilan solishtirishni to‘xtat.

Sen ularning yo‘lini emas, o‘zingga berilgan yo‘lni bosib o‘tyapsan.

Sekin ketayotgan bo‘lsang ham, ortga qaytmayotganing muhim."""

    await update.message.reply_text(text)


bot_app.add_handler(CommandHandler("start", start))


loop = asyncio.new_event_loop()


def telegram_worker():
    asyncio.set_event_loop(loop)

    loop.run_until_complete(bot_app.initialize())
    loop.run_until_complete(bot_app.start())

    loop.run_until_complete(
        bot_app.bot.set_webhook(WEBHOOK_URL)
    )

    loop.run_forever()


@app.route("/")
def home():
    return "Ringtonlar bot ishlayapti!"


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    update = Update.de_json(data, bot_app.bot)

    asyncio.run_coroutine_threadsafe(
        bot_app.process_update(update),
        loop
    )

    return "OK"


if __name__ == "__main__":
    threading.Thread(
        target=telegram_worker,
        daemon=True
    ).start()

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
