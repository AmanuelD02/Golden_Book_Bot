import logging
import os

from telegram import (ReplyKeyboardMarkup,
                      ReplyKeyboardRemove, KeyboardButton, ParseMode)
from telegram.ext import (Updater, CommandHandler,
                          messagehandler, ConversationHandler)

# utils
from utils import(send_msg)
# token of Morgul_bot
TOKEN = os.environ.get("GOLDEN_BOOK_BOT_TOKEN")

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def main_menu_keyboard(update, context):
    menu_options = [
        [KeyboardButton('📚 SEND BOOK REQUESTS'),
         KeyboardButton('✍️ Submit your writing')],
        [KeyboardButton('Send Us Feedback')],
        [KeyboardButton('ADMIN Features')]
    ]
    keyboard = ReplyKeyboardMarkup(menu_options)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             parse_mode=ParseMode.MARKDOWN,
                             reply_markup=keyboard,
                             disable_web_page_preview=True)


# Start Command
def start_cmd(update, context):
    logger.info("Start Command")
    send_msg(update, context, text="Welcome to Golden Book Bot")
    main_menu_keyboard()


def main():
    # create Updater and pass it to the bot's Token.
    updater = Updater(TOKEN, use_context=True)

    # Get The Dispatcher
    dp = updater.dispatcher

    # COMMAND HANDLER
    # Start
    start_handler = CommandHandler('start', start_cmd)

    # CONVERSATIONS HANDLER
    # Main Conversation
    main_conversation = ConversationHandler(entry_points=[start_handler],
                                            states={

    })
