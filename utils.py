# Send message function
def send_msg(update, context, text=""):
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)
