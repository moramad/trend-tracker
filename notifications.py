from telegram import ParseMode, Update, ForceReply
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Defaults, Filters, CallbackContext, CallbackQueryHandler
import requests, os
from dataCatcher import *
from dataModels import *
from dataAnalyze import *
from connSetting import *
from requests import get


TELEGRAM_TOKEN = telegramToken()

def checkPID():
    process = "notification"         
    nlist = 0
    for line in os.popen("ps ax | grep " + process + " | grep -v grep"):
        nlist += 1                    
    if nlist > 1:
        print("Application was started")
        exit()    

def telegram_sendMessage(bot_message):
   bot_token = TELEGRAM_TOKEN
   bot_chatID = telegramChatID()
   send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=HTML&text=' + bot_message

   response = requests.get(send_text)
   return response.json()

##########################################

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

##########################################
def pingCommand(update, context):        
    context.bot.send_message(chat_id=update.effective_chat.id, text='⚠️PONG')

def showIPCommand(update, context):        
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    ipAddress = get('https://api.ipify.org').content.decode('utf8')
    print(f"IP : {ipAddress}")
    context.bot.send_message(chat_id=update.effective_chat.id, text=ipAddress)

def helpCommand(update, context):
    response = f"<b>Menu Commands:</b> \n"
    response += f"/h, /help - This help menu \n"
    response += f"/ping - Check service bot \n"
    response += f"/p &#60;coin&#62; - Coin's Price \n"    
    response += f"/c &#60;coin&#62; - Coin's Chart \n"    
    response += f"/m - Market Summarize \n"
    response += f"/topcap - Top 10 by marketcap \n"
    response += f"/best - Top 10 by best performance\n"
    response += f"/worst - Top 10 by worst performance\n"
    response += f"/suggest - near 0% support \n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)

##########################################
def priceCommand(update, context):
    print(f"request from {update.effective_chat.username}")
    try:            
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        coin = context.args[0]        
        response = priceSummarize(coin)    
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)
    except:
        response = f"<b>Command Format:</b> \n"
        response += f"/p bitcoin\n"
        response += f"/p ethereum\n"
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)

def chartCommand(update, context):
    try:
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")    
        coin = context.args[0]
        print(coin)
        coin = coinStandardized(coin)
        print(f"request from {update.effective_chat.username} | request {coin}")    
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(f'chart/chart_{coin}.png', 'rb'))  
    except Exception as e:
        logger.error(f"An Error occured in chartCommand :: {e}")
        response = f"<b>File chart not found!</b> \n"
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)

def marketCommand(update, context):    
    print(f"request from {update.effective_chat.username}")
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    result = marketSummarize()    
    context.bot.send_message(chat_id=update.effective_chat.id, text=result)

def topcapCommand(update, context):
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    print(f"request from {update.effective_chat.username}")    
    result = topcapSummarize()    
    context.bot.send_message(chat_id=update.effective_chat.id, text=result)

def bestCommand(update, context):
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    print(f"request from {update.effective_chat.username}")    
    result = bestSummarize()
    context.bot.send_message(chat_id=update.effective_chat.id, text=result)

def worstCommand(update, context):
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    print(f"request from {update.effective_chat.username}")    
    result = worstSummarize()    
    context.bot.send_message(chat_id=update.effective_chat.id, text=result)

def suggestCommand(update, context):
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    print(f"request from {update.effective_chat.username}")
    coin = context.args[0]
    result = suggestSummarize(coin)    
    context.bot.send_message(chat_id=update.effective_chat.id, text=result)

##########################################
def start(update: Update, context: CallbackContext) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data='1'),
            InlineKeyboardButton("Option 2", callback_data='2'),
        ],
        [InlineKeyboardButton("Option 3", callback_data='3')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)

def button1(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    query.edit_message_text(text=f"Selected option1: {query.data}")

def button2(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    query.edit_message_text(text=f"Selected option2: {query.data}")

if __name__ == '__main__':
    checkPID()

    updater = Updater(token=TELEGRAM_TOKEN, defaults=Defaults(parse_mode=ParseMode.HTML))
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler("h", helpCommand))
    dispatcher.add_handler(CommandHandler("help", helpCommand))
    dispatcher.add_handler(CommandHandler("start", helpCommand))
    dispatcher.add_handler(CommandHandler("ip", showIPCommand))

    dispatcher.add_handler(CommandHandler("ping", pingCommand))        
    dispatcher.add_handler(CommandHandler("p", priceCommand))
    dispatcher.add_handler(CommandHandler("c", chartCommand))
    dispatcher.add_handler(CommandHandler("m", marketCommand))
    dispatcher.add_handler(CommandHandler("topcap", topcapCommand))
    dispatcher.add_handler(CommandHandler("best", bestCommand))
    dispatcher.add_handler(CommandHandler("worst", worstCommand))
    dispatcher.add_handler(CommandHandler("suggest", suggestCommand))

    # dispatcher.add_handler(CommandHandler('start', start))
    # dispatcher.add_handler(CallbackQueryHandler(button1, pattern='1'))
    # dispatcher.add_handler(CallbackQueryHandler(button2, pattern='2'))

    # dispatcher.add_handler(CommandHandler("alert", alertCommand))

    # dispatcher.add_handler(CommandHandler("coin", priceSummarizeCommand))
    # dispatcher.add_handler(CommandHandler("market", marketSummarizeCommand))      

    updater.start_polling() # Start the bot
    print("notification polling running")
        
    updater.idle() # Wait for the script to be stopped, this will stop the bot as well    
