from src.telegram_app import bot_app
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from flask import Flask, request

app = Flask(__name__)

application = bot_app()

@app.route('/webhook', methods=['POST'])
async def webhook():
    if request.method == 'POST':
        update = Update.de_json(request.get_json(force=True), application.bot)
        await application.process_update(update)
        return 'OK', 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
    # application.run_webhook(listen="0.0.0.0", port=5000)
