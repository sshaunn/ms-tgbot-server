from flask import Flask
import threading

from src.telegram_app import bot_app

app = Flask(__name__)


@app.route('/index', methods=['GET'])
def webhook():
    return 'OK', 200


if __name__ == '__main__':
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)).start()
    bot_app()
    # app.run_webhook(
    #     listen="0.0.0.0",
    #     port=5000,
    #     url_path=c.TOKEN,
    #     webhook_url=f"https://ms-tgbot-server.onrender.com/{c.TOKEN}"
    # )
    # application.run_webhook(listen="0.0.0.0", port=5000)
