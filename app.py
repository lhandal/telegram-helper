from flask import Flask, request
import telegram
from bot.credentials import bot_token, bot_username, URL
from bot.bot import get_response

global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    # get the chat_id to be able to respond to the same user
    chat_id = update.message.chat.id
    # get the message id to be able to reply to this specific message
    msg_id = update.message.message_id
    # Telegram understands UTF-8, so encode text for unicode compatibility
    incoming_message = update.message.text.encode('utf-8').decode()
    print("Got text message:", incoming_message)
    # here we call our super AI
    # response = get_response(incoming_message)
    get_response(incoming_message)
    # now just send the message back
    # notice how we specify the chat and the msg we reply to
    # bot.sendMessage(chat_id=chat_id, text=response, reply_to_message_id=msg_id)
    return 'ok'

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