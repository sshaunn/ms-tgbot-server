from telegram import Update, ChatMember, Bot
from telegram.ext import ContextTypes, ConversationHandler, Application
from telegram.error import TelegramError
# from pyrogram import Client
import src.consts as c
import src.validations as vld
from src.bitget.utils import get_current_date
from src.logger import log
from src.telegram_helper import extract_numeric_uid, create_group_invite_link
from src.service.customer_service import (get_customer_by_client_uid,
                                          save_customer,
                                          update_customer_membership,
                                          update_customer_ban_status,
                                          get_customer_by_key,
                                          get_customer_by_uid,
                                          update_customer_rejoin)

NEXT = range(1)
# api_id = "your_api_id"
# api_hash = "your_api_hash"
# bot_token = "your_bot_token"
# b = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)


async def check_customer_uid_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_type = update.message.chat.type
    message = update.message.text
    uid = extract_numeric_uid(message)
    customer = get_customer_by_client_uid(uid)

    if chat_type == 'private' and not message == "/cancel":

        if not vld.is_valid_uid(customer):
            log.error("UID is not matching, user_id=%s, user_name=%s", user.id, user.first_name)
            await update.message.reply_text(c.ERROR_MESSAGE_FROM_BOT)
            return ConversationHandler.END

        customer = save_customer(uid,
                                 user.first_name,
                                 user.last_name,
                                 user.id,
                                 customer['registerTime'],
                                 join_time=get_current_date())

        if not customer:
            await update.message.reply_text(c.ERROR_MESSAGE_FROM_BOT_DUPLICATED_UID_CHECK)
            await update.message.reply_text(c.FINISH_CONVERSATION_MESSAGE)
            return ConversationHandler.END

        membership = await context.bot.get_chat_member(chat_id=c.VIP_GROUP_ID, user_id=user.id)
        log.info("UID matching success, current user with UID=%s has membership=%s, and user=%s",
                 uid,
                 membership,
                 customer)

        if membership.status in [ChatMember.MEMBER, ChatMember.OWNER, ChatMember.ADMINISTRATOR]:
            update_customer_membership(uid, True)

        await update.message.reply_text(c.SUCCESS_MESSAGE_UID_CHECK)
    return ConversationHandler.END


async def start_customer_uid_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_type = update.message.chat.type
    message = update.message.text
    uid = extract_numeric_uid(message)
    customer = get_customer_by_client_uid(uid)

    if chat_type == 'private' and not message == "/cancel":

        if not vld.is_valid_uid(customer):
            log.error("UID is not matching, uid=%s, user_id=%s, user_name=%s", uid, user.id, user.first_name)
            await update.message.reply_text(c.ERROR_MESSAGE_FROM_BOT)
            return ConversationHandler.END

        # customer = get_customer_ban_status_by_uid(uid)
        # if customer['is_ban']:
        #     log.info("current user got banned, uid=%s, user_id=%s, user_name=%s", uid, user.id, user.first_name)
        #     await update.message.reply_text(c.ERROR_MESSAGE_FROM_BOT_USER_BANNED)
        #     return ConversationHandler.END

        if vld.is_exist_uid(uid):
            log.error("UID is exist, uid=%s, user_id=%s, user_name=%s, customer=%s", uid, user.id, user.first_name,
                      customer)
            await update.message.reply_text(c.ERROR_MESSAGE_FROM_BOT_USER_EXIST)
            return ConversationHandler.END

        customer = save_customer(uid,
                                 user.first_name,
                                 user.last_name,
                                 user.id,
                                 customer['registerTime'],
                                 join_time=get_current_date())

        invite = await create_group_invite_link(c.VIP_GROUP_ID, context)
        log.info("sending invite link to the user with uid=%s, user=%s", uid, customer)

        await update.message.reply_text(c.SUCCESS_MESSAGE_UID_CHECK)
        await update.message.reply_text(f"这是邀请链接: {invite.invite_link}")
    return ConversationHandler.END


async def reinvite_customer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_type = update.message.chat.type
    message = update.message.text
    uid = extract_numeric_uid(message)
    if message == "/cancel":
        return ConversationHandler.END
    customer = get_customer_by_uid(uid)
    if not vld.is_over_trade_volumn(uid) and not vld.is_ban(customer['left_time']):
        await update.message.reply_text(c.ERROR_MESSAGE_FROM_BOT_REJOIN)
        return ConversationHandler.END

    update_customer_rejoin(uid, False)
    invite = await create_group_invite_link(c.VIP_GROUP_ID, context)
    log.info("sending invite link to the user with uid=%s, user=%s", uid, customer)

    await update.message.reply_text(c.SUCCESS_MESSAGE_UID_CHECK)
    await update.message.reply_text(f"这是邀请链接: {invite.invite_link}")
    return ConversationHandler.END


async def check_customer_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = update.chat_member
    if result.new_chat_member.status in [ChatMember.MEMBER, ChatMember.OWNER, ChatMember.ADMINISTRATOR]:
        new_member = result.new_chat_member.user
        customer = get_customer_by_key('tgid', str(new_member.id))
        if customer:
            update_customer_membership(customer['uid'], True)
            log.info("current user with UID=%s, tgid=%s has membership", customer['uid'], new_member.id)


async def kick_group_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        uid = extract_numeric_uid(update.message.text)
        chat_id = c.VIP_GROUP_ID

        customer = get_customer_by_uid(uid)
        if not customer:
            log.error("current user with uid=%s not found", uid)
            return NEXT

        await context.bot.ban_chat_member(chat_id, customer['tgid'])
        await context.bot.unban_chat_member(chat_id, customer['tgid'])

        if customer:
            update_customer_ban_status(uid, False, True, get_current_date())
            log.info("current user with UID=%s, tgid=%s cancelled membership", uid, customer['tgid'])
    except ValueError:
        await update.message.reply_text('Please send a valid user ID.')
    except Exception as e:
        log.error(f'Error kicking user: {e}')
        await update.message.reply_text('An error occurred while trying to kick the user.')
    return ConversationHandler.END


async def send_heartbeat(context):
    await context.bot.send_message("-1002217128790", text="heartbeat")


async def kick_all_inactive_customers():
    # active_customers = get_all_customers_in_group_chat()
    # url_kick = f"{c.TELEGRAM_API_PREFIX}/kickChatMember"
    bot = Bot(c.TOKEN)

    try:
        members = await bot.get_chat(c.VIP_GROUP_ID)
        # for m in members:
        #     log.info(m.user)
        return members
    except TelegramError as e:
        print(f"Error: {e}")
        return None
