from telegram import ParseMode
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, Defaults
import requests

TELEGRAM_TOKEN = "1827426924:AAHja4wVzre72M04RRQG5vkOBBG48gIN6PE"


def telegram_sendMessage(bot_message):
   bot_token = TELEGRAM_TOKEN
   bot_chatID = '1282342719'
   send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

   response = requests.get(send_text)
   return response.json()

def startCommand(update, context):    
    context.bot.send_message(chat_id=update.effective_chat.id, text='Hello there!')

def priceAlert(update, context):
    if len(context.args) > 2:
        crypto = context.args[0].upper()
        sign = context.args[1]
        price = context.args[2]

        context.job_queue.run_repeating(priceAlertCallback, interval=15, first=15, context=[crypto, sign, price, update.message.chat_id])
        
        response = f"⏳ I will send you a message when the price of {crypto} reaches £{price}, \n"
        response += f"the current price of {crypto} is £{coinbase_client.get_spot_price(currency_pair=crypto + '-GBP')['amount']}"
    else:
        response = '⚠️ Please provide a crypto code and a price value: \n<i>/price_alert {crypto code} {> / &lt;} {price}</i>'
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)

def priceAlertCallback(context):
    crypto = context.job.context[0]
    sign = context.job.context[1]
    price = context.job.context[2]
    chat_id = context.job.context[3]

    send = False
    spot_price = coinbase_client.get_spot_price(currency_pair=crypto + '-GBP')['amount']

    if sign == '<':
        if float(price) >= float(spot_price):
            send = True
    else:
        if float(price) <= float(spot_price):
            send = True

    if send:
        response = f'👋 {crypto} has surpassed £{price} and has just reached <b>£{spot_price}</b>!'

        context.job.schedule_removal()

        context.bot.send_message(chat_id=chat_id, text=response)

if __name__ == '__main__':
    updater = Updater(token=TELEGRAM_TOKEN, defaults=Defaults(parse_mode=ParseMode.HTML))
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", startCommand))
    dispatcher.add_handler(CommandHandler("alert", priceAlert)) # Accessed via /alert

    updater.start_polling() # Start the bot
        
    updater.idle() # Wait for the script to be stopped, this will stop the bot as well
