def get_response(msg):
    """
    you can place your mastermind AI here
    could be a very basic simple response like "معلش"
    or a complex LSTM network that generate appropriate answer
    """

    if msg.lower() == 'hola':
        text = 'Hola!'
    else:
        text = "......"
    bot.sendMessage(chat_id=chat_id, text=text, reply_to_message_id=msg_id)