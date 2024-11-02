import requests
import random
import time

TELEGRAM_TOKEN = ''
URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/"

wishes = [
    "Удачи!",
    "Хорошего дня!",
    "Пусть всё сложится!",
    "Отличного настроения!",
    "Пусть день будет ярким и радостным!"
]

def send_message(chat_id, text):
    url = URL + 'sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(url, json=payload)

def handle_updates():
    last_update_id = None
    started = False

    while True:
        url = URL + 'getUpdates'
        if last_update_id:
            url += f"?offset={last_update_id + 1}"
        response = requests.get(url)
        updates = response.json().get('result', [])

        for update in updates:
            last_update_id = update['update_id']
            message = update.get('message', {})
            chat_id = message.get('chat', {}).get('id')
            text = message.get('text', '')

            if not started:
                send_message(chat_id, "Привет! Я бот, который отправляет пожелания на день. "
                                      "Чтобы получить пожелание, отправьте команду /day.")
                started = True

            if text == '/day':
                wish = random.choice(wishes)
                send_message(chat_id, wish)

        time.sleep(1)

if __name__ == '__main__':
    handle_updates()
