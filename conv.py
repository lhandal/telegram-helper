from credentials import bot_token
import logging
from helper_functions import *

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

SEARCH_TYPE, TYPE, CHOSEN  = range(3)


def books(update, context):
    reply_keyboard = [['Title', 'Author']]

    update.message.reply_text(
        'Hi! My name is Professor Bot. I will hold a conversation with you. '
        'Send /cancel to stop talking to me.\n\n'
        'How do you want to search?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return SEARCH_TYPE


def search_type(update, context):
    user = update.message.from_user
    logger.info("Search type of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(f'Thank you! Please type the *{update.message.text.lower()}* then.',
                              parse_mode=ParseMode.MARKDOWN)
    global s_type
    s_type = update.message.text.lower()
    return TYPE


def choose(update, context):
    user = update.message.from_user
    logger.info("Query of %s: %s", user.first_name, update.message.text)
    print(s_type)
    print(update.message.text)
    results = filter_results(search_book(by=s_type, value=update.message.text))
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

    return CHOSEN


def sent(update, context):
    user = update.message.from_user
    global chosen
    chosen = int(re.findall(r'\d+', update.message.text)[0]) - 1
    logger.info(f"{user.first_name} selected option {chosen} from list.")
    print(s_type, s_value, chosen)
    url = get_book_link(search_book(by=s_type, value=s_value)[chosen])

    update.message.reply_text(f'Here you go, {user.first_name}, here is your link!\n\n{url}')

    return ConversationHandler.END


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! Let me know if you need anything else!.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(bot_token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('books', books)],
        states={
            SEARCH_TYPE: [MessageHandler(Filters.regex('^(Title|Author)$'), search_type)],

            TYPE: [MessageHandler(Filters.text, choose)],

            CHOSEN: [MessageHandler(Filters.text, sent)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()