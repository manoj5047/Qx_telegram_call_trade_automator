import telegram
from telegram.ext import CommandHandler
# Start bot and add message handler
from telegram.ext import Updater, MessageHandler, Filters

# Telegram Bot API token
telegram_token = '6080468788:AAFrPTaNdyzx_6nNGzQb3Gqfc16iSS_9R00'

# Create Telegram bot instance
bot = telegram.Bot(token=telegram_token)

updater = Updater(token=telegram_token, use_context=True)
dispatcher = updater.dispatcher


def list_channels(update, context):
    print("Called")

    channels = context.bot.get_chat_members_count(chat_id='@my_channel')['result']
    print(f"My bot is a member of {len(channels)} channels:")
    for channel in channels:
        print(channel['chat']['title'])


# Define message handler
def handle_message(update, context):
    # Get chat ID and message text
    chat_id = update.effective_chat.id
    message_text = update.message.text

    # Send reply message
    bot.send_message(chat_id=chat_id, text=f"Hello, {message_text}!")


def receive_message(update, context):
    message = update.message
    # Do something with the message here, e.g. print it to the console
    print(f"Received message: {message.text}")


def message_handler(update, context):
    print(update.message)
    # # Get the user ID and the message text
    # # user_id = update.message.
    # message_text = update.message.text
    #
    # # Do something with the message (e.g. print it)
    # print(f"New message from user : {message_text}")
    message = update.message
    if message.chat.type == 'group':
        print(f'Received message in group {message.chat.title}: {message.text}')


def handle_error(update, context):
    # Log the error message
    updater.logger.error("Exception while handling an update:", exc_info=context.error)
    # Send a friendly error message to the user
    context.bot.send_message(chat_id=update.message.chat_id, text="Oops, something went wrong!")


def main():
    # Create a Telegram bot object
    bot = telegram.Bot(token=telegram_token)

    # Create an updater object and pass it the bot object
    updater = Updater(token=telegram_token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), message_handler))
    dp.add_error_handler(handle_error)

    # Register the message handler function to handle incoming messages
    # print(f"New message from user : {Filters.text}")
    # updater.dispatcher.add_handler(MessageHandler(filters=Filters.text, callback=message_handler))
    # Register the command handler
    list_channels_handler = CommandHandler('list_channels', list_channels)
    dispatcher.add_handler(list_channels_handler)
    # Start the bot
    updater.start_polling()
    updater.idle()


# Call the main function to start the bot
if __name__ == '__main__':
    main()
# updater = Updater(token=telegram_token, use_context=True)
# dispatcher = updater.dispatcher
# dispatcher.add_handler(MessageHandler(Filters.text, handle_message))
# updater.start_polling()
