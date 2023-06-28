import requests
import json
import telegram
import time

with open('BotToken.txt', 'r') as bottokenfile:
    bottoken = bottokenfile.read().strip()
with open('ChatID.txt', 'r') as chatidfile:
    chatid = chatidfile.read().strip()

f = open('wsparcie2.json', 'r+')
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

    # OfferStart = stringus.find("/oferta", stringus.rfind("adCard-featured"))
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
    # if stringus.rfind("adCard-featured") != -1:
    #     OfferStart = stringus.find("/oferta", stringus.rfind("adCard-featured"))
    # else:
    #     OfferStart = stringus.find("/oferta", )

    # OfferStart = stringus.find("/oferta", stringus.rfind("adCard-featured"))

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

        for i in range(0, len(data['rzeczy'])):

            print(data['rzeczy'][i]['nazwa'])
            try:
                x = decidepull(data['rzeczy'][i]['link'])
                print(x)
                first = decidefirst(data['rzeczy'][i]['link'])
                if int(x) != int(data['rzeczy'][i]['liczba']):
                    if int(x) > int(data['rzeczy'][i]['liczba']):
                        bot.send_message(chat_id=chatid, text=(str(data['rzeczy'][i]['nazwa']) + " " + str(x)))
                        # update.message.reply_text((str(data['rzeczy'][i]['link'])))
                        bot.send_message(chat_id=chatid, text=first)
                    data['rzeczy'][i]['liczba'] = x
                    w = json.dumps(data)
                    with open("wsparcie2.json", 'w') as f:
                        f.write(w)
            except Exception as e:
                print(e)
                time.sleep(600)
        time.sleep(30)






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
zacznijolxowac()
# print(int((stringus[indexOfFound + 11] + stringus[indexOfFound + 12] + stringus[indexOfFound + 13] + stringus[indexOfFound + 14] + stringus[indexOfFound + 15])))

f.close()
