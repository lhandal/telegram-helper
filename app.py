from flask import Flask, request
import telegram
from credentials import bot_token, bot_username, URL
from bot import *
from helper_functions import *
from telegram.ext import Updater, CommandHandler


global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

def hello(update, context):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))

@app.route('/{}'.format(TOKEN), methods=['POST'])
# def respond():
    # Retrieve the message in JSON and then transform it to Telegram object
    # update = telegram.Update.de_json(request.get_json(force=True), bot)
    # incoming_message, msg_id, chat_id, name, lastname = parse_message(update)


updater = Updater(TOKEN, use_context=True)
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.start_polling()
updater.idle()
    #x
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