# worker: python script.py --> Procfile
# heroku ps:scale worker=1 --> CLI
from telegram import InlineQueryResultArticle, InputTextMessageContent, ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters, ConversationHandler
from credentials import bot_token
from helper_functions import *
from texts import *
import logging
from helper_functions import *

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

SEARCH_TYPE, CHOOSE, SENT, ROAST = range(4)


def start(update, context):
    chat_id = update.effective_chat.id
    user = update.message.from_user
    user_id, name, lastname, username = user.id, user.first_name, user.last_name, user.username
    text = start_text(name)
    context.bot.send_message(chat_id=chat_id, text=text)
    logger.info(f"{user.first_name} {user.last_name} selected option /start.")

def doggo(update, context):
    user = update.message.from_user
    url = get_image_url()
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=url)
    logger.info(f"{user.first_name} {user.last_name} selected option /doggo.")


def gangsta(update, context):
    user = update.message.from_user
    if context.args:
        gangsta_text = gangstarize(' '.join(context.args))
        context.bot.send_message(chat_id=update.effective_chat.id, text=gangsta_text)
    elif not context.args:
        text = 'Please add your text after /gangsta\ni.e. /gangsta How are you?'
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    logger.info(f"{user.first_name} {user.last_name} selected option /gangsta.")

def rateme(update, context):
    user = update.message.from_user
    logger.info(f"{user.first_name} {user.last_name} selected option /rateme.")
    update.message.reply_text('Send me a photo of yourself! 👀',
                              reply_markup=ReplyKeyboardRemove())
    return ROAST

def roast(update, context):
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_photo.jpg')
    logger.info(f"{user.first_name} {user.last_name} sent: 'user_photo.jpg'")
    roast = get_roast(user.first_name)
    update.message.reply_text(f'{user.first_name}, {roast}')

    return ConversationHandler.END


def inline_caps(update, context):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)


def books(update, context):
    user = update.message.from_user
    reply_keyboard = [['Title', 'Author']]
    logger.info(f"{user.first_name} {user.last_name} selected option /books.")
    update.message.reply_text(
        f'''I can help you download most books! 📚
'Do you want to search by *title* or *author*?''',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    parse_mode=ParseMode.MARKDOWN)

    return SEARCH_TYPE


def search_type(update, context):
    user = update.message.from_user
    update.message.reply_text(f'Thank you!\nPlease type the *{update.message.text.lower()}* then.',
                              parse_mode=ParseMode.MARKDOWN)
    logger.info(f"Search type of {user.first_name} {user.last_name} {update.message.text}")
    global s_type
    s_type = update.message.text.lower()
    return CHOOSE


def choose(update, context):
    user = update.message.from_user
    logger.info(f"Query of {user.first_name} {user.last_name}: {update.message.text}")
    results = filter_results(search_book(by=s_type, value=update.message.text))
    if len(results) > 0:
        global s_value
        s_value = update.message.text
        update.message.reply_text(f'I got these results for {s_value}, which of the following do you want?\nTell me the result number you want to download.')
        n = 1
        for result in results:
            text = f"""*Result {n}*
        Title: {result['Title']}
        Author: {result['Author']}
        Publisher: {result['Publisher']}
        Year: {result['Year']}
        Language: {result['Language']}
        Pages: {result['Pages']}
        Size: {result['Size']}
        Extension: {result['Extension']}"""
            print(text)
            n += 1
            update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
            if n == 25:
                break
        update.message.reply_text(f'''Which of those do you like?\n
Tell me the *result number* you want to download!\n
Type /cancel to cancel search.''', parse_mode=ParseMode.MARKDOWN)
        return SENT
    else:
        logger.info(f"{user.first_name} {user.last_name}'s query got no results.")
        update.message.reply_text('Your query got 0 results, please try again... \n\nSend *another query* or /cancel to cancel search.',
                                  reply_markup=ReplyKeyboardRemove(), parse_mode=ParseMode.MARKDOWN)
        return CHOOSE


def sent(update, context):
    user = update.message.from_user

    if update.message.text != '/cancel':
        global chosen
        chosen = int(re.findall(r'\d+', update.message.text)[0]) - 1
        logger.info(f"{user.first_name} {user.last_name} selected option {chosen+1} from list.")
        print(s_type, s_value, chosen+1)
        url = get_book_link(search_book(by=s_type, value=s_value)[chosen])
        update.message.reply_text(f'Here you go {user.first_name}, here is your link!\n\n{url}')
        return ConversationHandler.END
    else:
        logger.info(f"{user.first_name} {user.last_name} canceled the conversation.")
        update.message.reply_text('Bye! Let me know if you need anything else!',
                                  reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END



def cancel(update, context):
    user = update.message.from_user
    logger.info(f"{user.first_name} {user.last_name} canceled the conversation.")
    update.message.reply_text('Bye! Let me know if you need anything else!',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def main():
    updater = Updater(token=bot_token, use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('books', books),
                      CommandHandler('rateme', rateme)],
        states={
            SEARCH_TYPE: [MessageHandler(Filters.regex('^(Title|Author)$'), search_type)],

            CHOOSE: [MessageHandler(Filters.text, choose)],

            SENT: [MessageHandler(Filters.text, sent)],

            ROAST: [MessageHandler(Filters.photo, roast)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('doggo', doggo))
    dp.add_handler(CommandHandler('gangsta', gangsta))
    dp.add_handler(InlineQueryHandler(inline_caps))
    dp.add_handler(MessageHandler(Filters.command, unknown))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()
    updater.stop()

if __name__ == '__main__':
    print('running...')
    main()
