import datetime
import requests
import re
from tzlocal import get_localzone

# url = 'https://api.telegram.org/bot1372295846:AAEka6_LQCCEMMCYJ8SQyXXgJGW65xelC-I/'


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
tz = get_localzone()
now = datetime.datetime.now(tz)
operators = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
             }


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
            my_bot.send_message(last_chat_id, f'Доброе утро, {last_chat_name}')
            # today += 1

        elif last_chat_text.lower() in greetings and today == now.day and 12 <= hour < 17:
            my_bot.send_message(last_chat_id, f'Добрый день, {last_chat_name}')
            # today += 1

        elif last_chat_text.lower() in greetings and today == now.day and 17 <= hour < 23:
            my_bot.send_message(last_chat_id, f'Добрый вечер, {last_chat_name}')
            # today += 1
        else:
            try:
                operand_1, operator, operand_2 = re.split(r'([+\-*/])', last_chat_text)
                operand_1 = int(operand_1)
                operand_2 = int(operand_2)
                if operator in operators:
                    result = operators[operator](operand_1, operand_2)
                    my_bot.send_message(last_chat_id, f'{last_chat_text} = {result}')
            except ValueError:
                my_bot.send_message(last_chat_id, f'Я Вас не понимаю, {last_chat_name}')
        new_offset = last_update_id + 1


if __name__ == '__main__':
    main()
