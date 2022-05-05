import requests
import logging
from telegram.ext import Updater, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup

api_key = 'BbRsEHSykK71xnmxaHXyFJpXA_R8CoyJ6BK7n1zZqbDC0aT72P9aFsW5LfmhXjaH'


def make_request(textt):
    base_url = 'https://api.genius.com'
    search_url = base_url + '/search'
    data = {'q': textt,
            'access_token': api_key}
    responses = requests.get(search_url, data=data)
    return responses.json()


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

TOKEN = '5333124058:AAHr1PL7sNjXOJRGpHvKjXemy7PiSZFa60g'
options = []
zxc = {}


def echo(update, context):
    global options
    global zxc

    z = update.message.text

    if z in options:
        print(zxc['response']['hits'])
        for i in zxc['response']['hits']:
            if i["result"]['full_title'] == z:
                update.message.reply_text(i["result"]["url"])
    else:
        options = []
        zxc = make_request(z)
        if zxc['response']['hits'] == []:
            update.message.reply_text("Песня не найдена")
        for i in zxc['response']['hits'][:5]:
            options.append(i["result"]['full_title'])
            update.message.reply_text(i["result"]['full_title'])
        reply_keyboard = [options]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        update.message.reply_text("Выберете песню:", reply_markup=markup)




def main():
    updater = Updater("5333124058:AAHr1PL7sNjXOJRGpHvKjXemy7PiSZFa60g")
    dp = updater.dispatcher
    text_handler = MessageHandler(Filters.text, echo)
    dp.add_handler(text_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
