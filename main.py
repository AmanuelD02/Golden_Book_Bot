import logging
import os

from telegram import (ReplyKeyboardMarkup,
                      ReplyKeyboardRemove, KeyboardButton, ParseMode)
from telegram.ext import (Updater, CommandHandler,
                          MessageHandler, ConversationHandler, Filters)

# utils
from utils import(send_msg)

# token of Morgul_bot
TOKEN = os.environ.get("GOLDEN_BOOK_BOT_TOKEN")

# Variables
ADMIN_NAMES = {123: "Amanuel", 456: "Mastewal"}
# STATE Variables
INTERMEDIATE = 1

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def main_menu_keyboard(update, context):
    menu_options = [
        [KeyboardButton('📚 SEND BOOK REQUESTS'),
         KeyboardButton('✍️ Submit your writing')],
        [KeyboardButton('📝 Send Us Feedback')],
        [KeyboardButton('🏴‍☠️ ADMIN Features')]
    ]
    keyboard = ReplyKeyboardMarkup(menu_options)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             parse_mode=ParseMode.MARKDOWN,
                             reply_markup=keyboard,
                             text="Welcome to Golden Book Bot",
                             disable_web_page_preview=True)


# Start Command
def start_cmd(update, context):
    logger.info("Start Command")
    # main_menu_keyboard(update, context)

    return INTERMEDIATE

# /book_request


def book_request(update, context):
    logger.info("Send Book Request")
    txt = "Please Enter The Book title and author."
    send_msg(update, context, text=txt, reply_markup=ReplyKeyboardRemove())


# /feedback


def feedback(update, context):
    logger.info("Feedback info")
    update.message.reply_text('Write Your Feedback below',
                              reply_markup=ReplyKeyboardRemove())

    return

# /Submit_essay


def Submit_essay(update, context):
    logger.info("Submit essay")
    txt = "Click the Button to indicate that you have read and agree to the terms of the Golden Book Customer Agreement."
    send_msg(update, context, text=txt, reply_markup=ReplyKeyboardRemove())

    return


def Admin_features(update, context):
    logging.info("Admin Only")
    admin_name = ADMIN_NAMES.get(update.effective_chat.id)

    send_msg(update, context, text=f'Welocme {admin_name} ',
             reply_markup=ReplyKeyboardRemove())

    return


def intermediate(update, context):
    logger.info("Intermediate ")
    choice = update.message.text
    choice_dict = {'📚 SEND BOOK REQUESTS': 0, '✍️ Submit your writing': 1,
                   '📝 Send Us Feedback': 2, '🏴‍☠️ ADMIN Features': 3}

    switch = choice_dict.get(choice)
    if switch == 0:
        book_request(update, context)
    elif switch == 1:
        Submit_essay(update, context)
    elif switch == 2:
        feedback(update, context)
    elif switch == 3:
        user = update.effective_chat.id
        if user in ADMIN_NAMES.keys():
            Admin_features(update, context)
    else:
        send_msg(update, context, text="Unkown Command")


def cancel_cmd(update, context):
    logger.info("cancel Conversation")
    send_msg(
        update, context, text="Current Procces is Cancelled!")

    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # create Updater and pass it to the bot's Token.
    updater = Updater(TOKEN, use_context=True)

    # Get The Dispatcher
    dp = updater.dispatcher

    # COMMAND HANDLER
    # Start
    start_handler = CommandHandler('start', start_cmd)
    cancel_handler = CommandHandler('cancel', cancel_cmd)

    # CONVERSATIONS HANDLER
    # Main Conversation
    main_conversation_handler = ConversationHandler(entry_points=[start_handler],
                                                    states={
        INTERMEDIATE: [MessageHandler(Filters.text, intermediate)]},
        fallbacks=[CommandHandler(
            'cancel', cancel_cmd)]

    )

    handlers = [start_handler, cancel_handler, main_conversation_handler]

    for handler in handlers:
        dp.add_handler(handler)

    # log all errors
    dp.add_error_handler(error)

    # start the bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
