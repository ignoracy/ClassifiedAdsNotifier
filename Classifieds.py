import requests
import json
import telegram
import time

with open('BotToken.txt', 'r') as bottokenfile:
    bottoken = bottokenfile.read().strip()
with open('ChatID.txt', 'r') as chatidfile:
    chatid = chatidfile.read().strip()

f = open('data.json', 'r+')
data = json.load(f)
f.close()

bot = telegram.Bot(token=bottoken)




def pullFromOlx(url):
    r = requests.get(url)
    stringus = r.text
    indexOfFound = stringus.find("Znaleźliśmy")

    result = int((stringus[indexOfFound + 11] + stringus[indexOfFound + 12] + stringus[indexOfFound + 13] + stringus[
        indexOfFound + 14]))

    return result


def pullFromOtomoto(url):
    return 0
    # r = requests.get(url)
    # stringus = r.text
    #
    # if stringus.find("Nie znaleziono dopasowań do wybranej lokalizacji. Rozszerzyliśmy Twój obszar wyszukiwania, aby wyświetlić podane wyniki.")<5000:
    #     return 0
    #
    # indexOfFound = stringus.find("Wszystkie (")
    #
    # result = int(stringus[stringus.find("(", indexOfFound)+1:stringus.find(")", indexOfFound)])
    #
    # return result


def findFirstFromOlx(url):
    r = requests.get(url)
    stringus = r.text
    if stringus.rfind("adCard-featured") != -1:
        OfferStart = stringus.find("/oferta", stringus.rfind("adCard-featured"))
    else:
        OfferStart = stringus.find("/oferta", )

    if stringus[OfferStart - 1] == "d":
        offerLink = "olx.pl"
    else:
        offerLink = "otomoto.pl"

    OfferEnd = stringus.find(".html", OfferStart)

    for i in range(OfferStart, OfferEnd + 5):
        offerLink += stringus[i]

    return offerLink

def findFirstFromOtomoto(url):
    r = requests.get(url)
    stringus = r.text
    OfferStart = stringus.find("/oferta/",stringus.find("data-highlight=false"))


    offerLink = "otomoto.pl"

    OfferEnd = stringus.find(".html", OfferStart)

    for i in range(OfferStart, OfferEnd + 5):
        offerLink += stringus[i]

    return offerLink



def decidepull(url):
    if url.find("olx")!=-1:
        return pullFromOlx(url)
    elif url.find("otomoto")!=-1:
        return pullFromOtomoto(url)

def decidefirst(url):
    if url.find("olx") != -1:
        return findFirstFromOlx(url)
    elif url.find("otomoto") != -1:
        return findFirstFromOtomoto(url)





def zacznijolxowac():
    print("olx")
    bot.send_message(chat_id=chatid, text='olx')
    while (1 == 1):

        for i in range(0, len(data['data'])):

            print(data['data'][i]['name'])
            try:
                x = decidepull(data['data'][i]['link'])
                print(x)
                first = decidefirst(data['data'][i]['link'])
                if int(x) != int(data['data'][i]['number']):
                    if int(x) > int(data['data'][i]['number']):
                        bot.send_message(chat_id=chatid, text=(str(data['data'][i]['name']) + " " + str(x)))
                        # update.message.reply_text((str(data['data'][i]['link'])))
                        bot.send_message(chat_id=chatid, text=first)
                    data['data'][i]['number'] = x
                    w = json.dumps(data)
                    with open("data.json", 'w') as f:
                        f.write(w)
            except Exception as e:
                print(e)
                time.sleep(600)
        time.sleep(30)







zacznijolxowac()

f.close()
