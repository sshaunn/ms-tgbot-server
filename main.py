from src.telegram_app import bot_app

application = bot_app()

if __name__ == '__main__':
    application.run_webhook(listen="0.0.0.0", port=5000)
