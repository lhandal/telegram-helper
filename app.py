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
Dispatcher = updater.dispatcher
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def helper():
    from telegram.ext import Updater, InlineQueryHandler, CommandHandler
    import requests
    import re
    from credentials import bot_token

    def get_url():
        contents = requests.get('https://random.dog/woof.json').json()
        url = contents['url']
        return url

    def get_image_url():
        allowed_extension = ['jpg', 'jpeg', 'png']
        file_extension = ''
        while file_extension not in allowed_extension:
            url = get_url()
            file_extension = re.search("([^.]*)$", url).group(1).lower()
        return url

    def bop(bot, update):
        url = get_image_url()
        chat_id = update.message.chat_id
        bot.send_photo(chat_id=chat_id, photo=url)

    def main():
        updater = Updater('YOUR_TOKEN')
        dp = updater.dispatcher
        dp.add_handler(CommandHandler('bop', bop))
        updater.start_polling()
        updater.idle()

    main()

    # # Retrieve the message in JSON and then transform it to Telegram object
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
    main()