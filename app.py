from flask import Flask, request
import telegram
from credentials import bot_token, bot_username, URL
from bot import *
from helper_functions import *
from telegram.ext import Updater, CommandHandler

from telegram.ext.commandhandler import CommandHandler
from telegram.ext.updater import Updater
from telegram.ext.dispatcher import Dispatcher
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.bot import Bot


global bot
global TOKEN
global updater
global Dispatcher

updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def helper():
    def start(update=Update, context=CallbackContext):
        """
        the callback for handling start command
        """
        # getting the bot from context
        bot: Bot = context.bot

        # sending message to the chat from where it has received the message
        bot.send_message(chat_id=update.effective_chat.id,
                         text="You have just entered start command")
    # register a handler (here command handler)
    dispatcher.add_handler(
        # it can accept all the telegram.ext.Handler, CommandHandler inherits Handler class
        # documentation: https://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.commandhandler.html#telegram-ext-commandhandler
        CommandHandler("start", start))

    # starting polling updates from Telegram
    # documentation: https://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.updater.html#telegram.ext.Updater.start_polling
    updater.start_polling()

    # Retrieve the message in JSON and then transform it to Telegram object
    # update = telegram.Update.de_json(request.get_json(force=True), bot)
    # print(update.message)
    # incoming_message, msg_id, chat_id, name, lastname = parse_message(update)
    #
    # print("Got text message:", incoming_message)
    # get_response(incoming_message, chat_id, msg_id, name, lastname)
    # return 'ok'

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    # we use the bot object to link the bot to our app which live
    # in the link provided by URL
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    # something to let us know things work
    if s:
        return "Webhook setup ok!"
    else:
        return "Webhook setup failed..."

@app.route('/')
def index():
    return 'App is running!'

if __name__ == '__main__':
    # note the threaded arg which allow
    # your app to have more than one thread
    app.run(threaded=True)