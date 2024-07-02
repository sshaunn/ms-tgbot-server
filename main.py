import asyncio
import src.consts as c
from src.telegram_app import bot_app, check, cancel, UID
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ChatMemberHandler
from flask import Flask, request

from src.telegram_helper import conversation_handler
from src.telegram_service import check_customer_uid_command, start_customer_uid_command, kick_group_member, \
    reinvite_customer, check_customer_membership

# app = Flask(__name__)

# application = bot_app()

application = Application.builder().token(c.TOKEN).build()
application.add_handler(conversation_handler(check, check_customer_uid_command, cancel, UID, 'check'))
application.add_handler(conversation_handler(check, start_customer_uid_command, cancel, UID, 'start'))
application.add_handler(conversation_handler(check, kick_group_member, cancel, UID, 'kick'))
application.add_handler(conversation_handler(check, reinvite_customer, cancel, UID, 'rejoin'))
application.add_handler(ChatMemberHandler(check_customer_membership, ChatMemberHandler.CHAT_MEMBER))


# @app.route('/webhook', methods=['POST'])
# async def webhook():
#     if request.method == 'POST':
#         update = Update.de_json(request.get_json(force=True), application.bot)
#         await application.process_update(update)
#         return 'OK', 200


if __name__ == '__main__':
    application.run_webhook(
        listen="0.0.0.0",
        port=5000,
        url_path=c.TOKEN,
        webhook_url=f"https://ms-tgbot-server.onrender.com/{c.TOKEN}"
    )
    # application.run_webhook(listen="0.0.0.0", port=5000)
