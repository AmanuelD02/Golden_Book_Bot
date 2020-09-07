import logging
import os

from telegram import (ReplyKeyboardMarkup,
                      ReplyKeyboardRemove, KeyboardButton, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler,
                          MessageHandler, ConversationHandler, Filters, CallbackQueryHandler)

# utils
from utils import(send_msg, json_to_txt,
                  search_book_by_author, search_book_by_title)

# token of Morgul_bot
TOKEN = os.environ.get("GOLDEN_BOOK_BOT_TOKEN")

# Variables
ADMIN_NAMES = {311644567: "Amanuel", 456: "Mastewal"}
# STATE Variables
INTERMEDIATE, SEARCH_BY, FEEDBACK, RESPONSE = range(4)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def main_menu_keyboard(update, context):
    menu_options = [
        [KeyboardButton('📚 SEND BOOK REQUESTS'),
         KeyboardButton('✍️ Submit your writing')],

        [KeyboardButton('📝 Send Us Feedback'),
         KeyboardButton('🏴‍☠️ ADMIN Features')],

        [KeyboardButton('Back')]
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
    # print(update.effective_chat.id)
    main_menu_keyboard(update, context)

    return INTERMEDIATE

# /book_request


def book_request(update, context):
    logger.info("Send Book Request")
    txt = "Do you want to search by Title or Author? Choose Below"
    author = InlineKeyboardButton(
        text="Search by Author", callback_data="search-author")
    title = InlineKeyboardButton(
        text="Search by Title", callback_data="search-title")

    send_msg(update, context, text=txt,
             reply_markup=InlineKeyboardMarkup([[title, author]]))


# /feedback


def feedback(update, context):
    logger.info("Feedback info")
    update.message.reply_text('Write Your Feedback below',
                              reply_markup=ReplyKeyboardRemove())

    return FEEDBACK

# /Submit_essay


def feedback_recieve(update, context):
    logger.info("Feedback Recieved func")
    logger.info(f'Message- {update.message.text}')
    context.bot.forward_message(chat_id=-1001427033230,
                                from_chat_id=update.message.chat_id,
                                message_id=update.message.message_id)

    logger.info("Message Sent")

    return RESPONSE


def Submit_essay(update, context):
    logger.info("Submit essay")
    txt = "Click the Button to indicate that you have read and agree to the terms of the Golden Book Customer Agreement."
    send_msg(update, context, text=txt, reply_markup=ReplyKeyboardRemove())

    return


def Admin_features(update, context):
    logging.info("Admin Only")
    user = update.effective_chat.id
    if user in ADMIN_NAMES.keys():
        admin_name = ADMIN_NAMES.get(update.effective_chat.id)
        send_msg(update, context, text=f'Welocme {admin_name} ',
                 reply_markup=ReplyKeyboardRemove())
    else:
        send_msg(update, context, text="You are not authorized!",
                 reply_markup=ReplyKeyboardRemove())
        start_cmd(update, context)
        return

    return


def intermediate(update, context):
    logger.info("Intermediate ")
    choice = update.message.text
    choice_dict = {'📚 SEND BOOK REQUESTS': 0, '✍️ Submit your writing': 1,
                   '📝 Send Us Feedback': 2, '🏴‍☠️ ADMIN Features': 3, "Cancel": 4}

    switch = choice_dict.get(choice)
    if switch == 0:
        book_request(update, context)
    elif switch == 1:
        Submit_essay(update, context)
    elif switch == 2:
        feedback(update, context)
    elif switch == 3:
        Admin_features(update, context)
    elif switch == 4:
        cancel_cmd(update, context)

    else:
        send_msg(update, context, text="")

# In this function the user sends the author or title to the function


def book_search(update, context):
    logger.info("Search Book Button")
    query_data = update.callback_query.data
    context.bot.answer_callback_query(update.callback_query.id)

    context.user_data['search_by'] = query_data

    if query_data == "search-title":
        send_msg(update, context, text="Please enter the title of the book")
    else:
        send_msg(update, context, text="Please enter the Author")

    return SEARCH_BY


def search_book_conv(update, context):
    logger.info("Search book conversation message reciever")
    search_by = context.user_data['search_by']
    context.user_data.clear()

    if search_by == "search-title":
        title = update.message.text
        logger.info(f'Title - {title}')
        results = json_to_txt(search_book_by_title(title))

    else:
        author = update.message.text
        logger.info(f'Author - {author}')
        results = json_to_txt(search_book_by_author(author))

    del search_by
    for result in results:
        logger.info(result)
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=result, parse_mode=ParseMode.HTML)

    return ConversationHandler.END


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
    dispatcher = updater.dispatcher

    # COMMAND HANDLER

    cancel_handler = CommandHandler('cancel', cancel_cmd)
    book_request_handler = CommandHandler('book_request', book_request)
    #feedback_handler = CommandHandler('feedback', feedback)
    admin_handler = CommandHandler('admin', Admin_features)
    submit_essay_handler = CommandHandler('submit_writing', Submit_essay)

    # CallBack  Handler

    # CONVERSATIONS HANDLER
    # Main Conversation
    main_conv_handler = ConversationHandler(entry_points=[CommandHandler('start', start_cmd)],
                                            states={
        INTERMEDIATE: [MessageHandler(Filters.text, intermediate)]
    },
        fallbacks=[cancel_handler])

    # Search book

    search_book_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(book_search, pattern="search-")],
        states={
            SEARCH_BY: [MessageHandler(Filters.text, search_book_conv)]},
        fallbacks=[cancel_handler])

    # FeedBack
    feedback_conversation_handler = ConversationHandler(entry_points=[CommandHandler('feedback', feedback)],
                                                        states={
        FEEDBACK: [MessageHandler(Filters.text, feedback_recieve)]
    },
        fallbacks=[cancel_handler])

    handlers = [cancel_handler,
                main_conv_handler, book_request_handler,
                admin_handler, submit_essay_handler,
                search_book_handler, feedback_conversation_handler]

    for handler in handlers:
        dispatcher.add_handler(handler)

    dispatcher.add_handler(start_handler)
    # log all errors
    dispatcher.add_error_handler(error)

    # start the bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
