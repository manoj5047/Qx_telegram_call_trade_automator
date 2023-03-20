from telegram.ext import Updater, MessageHandler, Filters
# import MetaTrader4 as mt4


def read_message(update, context):
    message = update.message.text
    # do something with the message, e.g. extract trade information


def place_trade(symbol, trade_type, lots, stop_loss, take_profit):
    order = mt4.OrderSend(symbol=symbol, cmd=trade_type, volume=lots, sl=stop_loss, tp=take_profit)
    return order


updater = Updater(token='6080468788:AAFrPTaNdyzx_6nNGzQb3Gqfc16iSS_9R00', use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(Filters.chat('Cryptotab_Trading_BTC_Signals'), read_message))
updater.start_polling()
