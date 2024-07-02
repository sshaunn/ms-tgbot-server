from src.telegram_app import bot_app

# app = Flask(__name__)

# @app.route('/webhook', methods=['POST'])
# async def webhook():
#     if request.method == 'POST':
#         update = Update.de_json(request.get_json(force=True), application.bot)
#         await application.process_update(update)
#         return 'OK', 200


if __name__ == '__main__':
    bot_app()
    # app.run_webhook(
    #     listen="0.0.0.0",
    #     port=5000,
    #     url_path=c.TOKEN,
    #     webhook_url=f"https://ms-tgbot-server.onrender.com/{c.TOKEN}"
    # )
    # application.run_webhook(listen="0.0.0.0", port=5000)
