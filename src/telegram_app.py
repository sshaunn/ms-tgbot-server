from telegram.error import TelegramError

from src.logger import log
import src.consts as c
import src.validations as vld

from src.telegram_helper import conversation_handler
from src.telegram_service import (check_customer_uid_command,
                                  start_customer_uid_command,
                                  check_customer_membership,
                                  kick_group_member,
                                  reinvite_customer,
                                  send_heartbeat)
from telegram import ForceReply, Update, ChatMember, Bot
from telegram.ext import (CommandHandler,
                          ContextTypes,
                          MessageHandler,
                          filters,
                          ConversationHandler,
                          ChatMemberHandler,
                          Application)

UID = range(2)


async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    await update.message.reply_text("开始验证Bitget-UID,请输入你的数字UID:")
    return UID


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    log.info(20, "User with id=%s, name=%s canceled the conversation.", user.id, user.first_name)
    await update.message.reply_text('您已终止对话,感谢关注,祝您交易顺利!')
    return ConversationHandler.END


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


def bot_app():
    """Start the bot."""
    application = Application.builder().token(c.TOKEN).build()
    application.add_handler(conversation_handler(check, check_customer_uid_command, cancel, UID, 'check'))
    application.add_handler(conversation_handler(check, start_customer_uid_command, cancel, UID, 'start'))
    application.add_handler(conversation_handler(check, kick_group_member, cancel, UID, 'kick'))
    application.add_handler(conversation_handler(check, reinvite_customer, cancel, UID, 'rejoin'))
    application.add_handler(ChatMemberHandler(check_customer_membership, ChatMemberHandler.CHAT_MEMBER))
    application.job_queue.run_repeating(send_heartbeat, interval=1800, first=1800)
    # check_conversation_handler()
    #
    # # on different commands - answer in Telegram
    # application.add_handler(CommandHandler("start", start))
    # application.add_handler(CommandHandler("help", help_command))
    #
    # # on non command i.e message - echo the message on Telegram
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, save_customer_command))
    # return application
    # application.start()
    # Run the bot until the user presses Ctrl-C

    application.run_polling(allowed_updates=Update.ALL_TYPES)
    # return application
