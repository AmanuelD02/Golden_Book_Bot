# Send message function
def send_msg(update, context, text="", reply_markup=None):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)
