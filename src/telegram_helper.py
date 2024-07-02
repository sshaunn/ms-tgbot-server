import re

from src.logger import log
from src.service.customer_service import update_customer_membership
from telegram import ForceReply, Update, ChatMember
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler


def extract_numeric_uid(input_uid):
    return ''.join(re.findall(r'\d+', input_uid))


async def create_group_invite_link(group_id, context: ContextTypes.DEFAULT_TYPE):
    try:
        invite_link = await context.bot.create_chat_invite_link(chat_id=group_id, member_limit=1)
        return invite_link
    except Exception as ex:
        log.error("Error occurred when creating invite link, exception=%s", ex)
        return None


def conversation_handler(start_handler, msg_handler, cancel_handler, states, cmd):
    return ConversationHandler(
        entry_points=[CommandHandler(cmd, start_handler)],
        states={
            states: [MessageHandler(filters.TEXT & ~filters.COMMAND, msg_handler)]
        },
        fallbacks=[CommandHandler('cancel', cancel_handler)]
    )


def update_new_user_membership(update: Update, context: ContextTypes.DEFAULT_TYPE, uid):
    result = update.chat_member
    if result.new_chat_member.status in [ChatMember.MEMBER, ChatMember.OWNER, ChatMember.ADMINISTRATOR]:
        update_customer_membership(uid, True)
