from flask import Flask, request
import telegram
from bot.credentials import bot_token, bot_username, URL
from bot.bot import get_response
from telegram.ext import Updater, CommandHandler

global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

updater = Updater(token='TOKEN', use_context=True)
dispatcher = updater.dispatcher
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.start_polling()

@app.route('/{}'.format(TOKEN), methods=['POST'])
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


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

# def respond():
#     # retrieve the message in JSON and then transform it to Telegram object
#     update = telegram.Update.de_json(request.get_json(force=True), bot)
#     chat_id = update.message.chat.id
#     msg_id = update.message.message_id
#     # Telegram understands UTF-8, so encode text for unicode compatibility
#     incoming_message = update.message.text.encode('utf-8').decode()
#     print("Got text message:", incoming_message)
#     get_response(incoming_message, chat_id, msg_id)
#     return 'ok'