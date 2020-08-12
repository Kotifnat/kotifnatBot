import re

import requests
import datetime


class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=None):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self, offset):
        get_result = self.get_updates(offset)

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = None

        return last_update


token = '1372295846:AAEka6_LQCCEMMCYJ8SQyXXgJGW65xelC-I'
my_bot = BotHandler(token)
greetings = ('здравствуй', 'привет', 'ку', 'здорово')
now = datetime.datetime.now()
operators = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
             }


def main():
    new_offset = None
    hour = now.hour

    while True:

        last_update = my_bot.get_last_update(new_offset)

        if last_update:
            last_update_id = last_update['update_id']
            last_chat_text = last_update['message']['text']
            last_chat_id = last_update['message']['chat']['id']
            last_chat_name = last_update['message']['chat']['first_name']

            if last_chat_text.lower() in greetings and 6 <= hour < 12:
                my_bot.send_message(last_chat_id, 'Доброе утро, {}'.format(last_chat_name))

            elif last_chat_text.lower() in greetings and 12 <= hour < 17:
                my_bot.send_message(last_chat_id, 'Добрый день, {}'.format(last_chat_name))

            elif last_chat_text.lower() in greetings and 17 <= hour < 23:
                my_bot.send_message(last_chat_id, 'Добрый вечер, {}'.format(last_chat_name))
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
    try:
        main()
    except KeyboardInterrupt:
        exit()
