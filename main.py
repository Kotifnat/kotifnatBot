import datetime
import requests


url = 'https://api.telegram.org/bot1372295846:AAEka6_LQCCEMMCYJ8SQyXXgJGW65xelC-I/'


class MyBot:

    def __init__(self, token):
        self.token = token
        self.api_url = f'https://api.telegram.org/bot{token}/'

    def get_updates(self, timeout=45, offset=None):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        response = requests.get(self.api_url + method, data=params).json()
        return response['result']

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        response = requests.post(self.api_url + method, data=params)
        return response

    def get_last_update(self):
        result = self.get_updates()

        if len(result) > 0:
            last_update = result[-1]
        else:
            last_update = result[len(result)]
        return last_update


token_api = '1372295846:AAEka6_LQCCEMMCYJ8SQyXXgJGW65xelC-I'
my_bot = MyBot(token=token_api)
greetings = ("здравствуй", "ку", "привет")
now = datetime.datetime.now()


def main():
    new_offset = None
    today = now.day
    hour = now.hour

    while True:
        my_bot.get_updates(offset=new_offset)

        last_update = my_bot.get_last_update()

        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']

        if last_chat_text.lower() in greetings and today == now.day and 6 <= hour < 12:
            my_bot.send_message(last_chat_id, 'Доброе утро, {}'.format(last_chat_name))
            # today += 1

        elif last_chat_text.lower() in greetings and today == now.day and 12 <= hour < 17:
            my_bot.send_message(last_chat_id, 'Добрый день, {}'.format(last_chat_name))
            # today += 1

        elif last_chat_text.lower() in greetings and today == now.day and 17 <= hour < 23:
            my_bot.send_message(last_chat_id, 'Добрый вечер, {}'.format(last_chat_name))
            # today += 1

        new_offset = last_update_id + 1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
