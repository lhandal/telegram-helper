import telegram
from credentials import bot_token, bot_username, URL
from telegram.ext import CommandHandler
from helper_functions import *


global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

def parse_message(update):
    # Payload vars
    chat_id = update.message.chat.id
    name, lastname = update.message.chat.first_name, update.message.chat.last_name
    msg_id = update.message.message_id
    incoming_message = normalize_text(update.message.text.encode('utf-8').decode())
    return incoming_message, msg_id, chat_id, name, lastname


def get_response(msg, chat_id, msg_id, name, lastname):

    if any(word in msg.lower() for word in ['hola', 'juan', 'hi']):
    # if msg.lower() in ['hola', 'juan', 'hi', 'juan?']:
        text = f'Hello {name}! \nWhat can I do for you today?'
    else:
        text = "......"

    bot.sendMessage(chat_id=chat_id, text=text)  # , reply_to_message_id=msg_id)
