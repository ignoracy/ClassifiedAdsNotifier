import requests
import json
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from telegram import Bot
import time

f = open('wsparcie2.json', 'r+')
data = json.load(f)
f.close()
# bot = Bot("")


updater = Updater("ENTER YOUR BOT TOKEN HERE", use_context=True)
#url = "https://www.olx.pl/d/motoryzacja/samochody/poznan/q-bmw-e36/?search%5Bdistrict_id%5D=719&search%5Bdist%5D=100&search%5Bfilter_float_price:to%5D=15000&search%5Bfilter_float_year:to%5D=2000"


def pullFromOlx(url):
    r = requests.get(url)
    stringus = r.text
    indexOfFound = stringus.find("Znaleźliśmy")

    result = int((stringus[indexOfFound + 11] + stringus[indexOfFound + 12] + stringus[indexOfFound + 13] + stringus[
        indexOfFound + 14]))

    return result


def findFirstFromOlx(url):
    r = requests.get(url)
    stringus = r.text

    OfferStart = stringus.rfind("/oferta", stringus.find("adCard-featured"), stringus.find("Dzisiaj"))
    if stringus[OfferStart-1]=="d":
        offerLink = "olx.pl"
    else:
        offerLink = "otomoto.pl"

    OfferEnd = stringus.find(".html", OfferStart)

    for i in range(OfferStart, OfferEnd + 5):
        offerLink += stringus[i]

    return offerLink


def start(update: Update, context: CallbackContext):
    update.message.reply_text("witaj u ignasiowego bota")


def ping(update: Update, context: CallbackContext):
    update.message.reply_text("pong")


def zacznijolxowac(update: Update, context: CallbackContext):
    print("olx")
    update.message.reply_text("olx")
    while (1 == 1):

        for i in range(0, len(data['rzeczy'])):

            print(data['rzeczy'][i]['nazwa'])
            try:
                print(pullFromOlx(data['rzeczy'][i]['link']))
                if int(pullFromOlx(data['rzeczy'][i]['link'])) != int(data['rzeczy'][i]['liczba']):
                    if int(pullFromOlx(data['rzeczy'][i]['link'])) > int(data['rzeczy'][i]['liczba']):
                        update.message.reply_text(
                            (str(data['rzeczy'][i]['nazwa']) + " " + str(pullFromOlx(data['rzeczy'][i]['link']))))
                        # update.message.reply_text((str(data['rzeczy'][i]['link'])))
                        update.message.reply_text(findFirstFromOlx(data['rzeczy'][i]['link']))
                    data['rzeczy'][i]['liczba'] = pullFromOlx(data['rzeczy'][i]['link'])
                    w = json.dumps(data)
                    with open("wsparcie2.json", 'w') as f:
                        f.write(w)
            except Exception as e:
                print(e)
        time.sleep(30)





updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('ping', ping))
updater.dispatcher.add_handler(CommandHandler('olx', zacznijolxowac))

updater.start_polling()
# url = "https://stackoverflow.com/questions/24297257/save-html-of-some-website-in-a-txt-file-with-python"
# url = "https://www.olx.pl/d/motoryzacja/samochody/poznan/q-bmw-e36/?search%5Bdistrict_id%5D=719&search%5Bdist%5D=100&search%5Bfilter_float_price:to%5D=15000&search%5Bfilter_float_year:to%5D=2000"
# url = "https://www.olx.pl/d/motoryzacja/samochody/q-bmw-e60/"

# with open('file.txt', 'w+', encoding="utf=8") as file:
# file.write(r.text)

# print(len(stringus))
# print(indexOfFound)
'''
for item in data['rzeczy']:
    print(item['nazwa'])
    print(pullFromOlx(item['link']))
    if int(pullFromOlx(item['link'])) != int(item['liczba']):
        bot.send_message(chatid = text= (str(item['nazwa'])+" "+str(item['liczba'])))
        item['liczba'] = str(pullFromOlx(item['link']))

'''

# print(int((stringus[indexOfFound + 11] + stringus[indexOfFound + 12] + stringus[indexOfFound + 13] + stringus[indexOfFound + 14] + stringus[indexOfFound + 15])))

f.close()
