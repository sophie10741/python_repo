import requests
import time

TELEGRAM_TOKEN = ''
YANDEX_API_KEY = ''
YANDEX_CATALOG_ID = ''
URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/"

def translate_text(text, source_language='ru', target_language='en'):
    url = 'https://translate.api.cloud.yandex.net/translate/v2/translate'
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {YANDEX_API_KEY}"
    }
    payload = {
        "sourceLanguageCode": source_language,
        "targetLanguageCode": target_language,
        "format": "HTML",
        "texts": [text],
        "folderId": YANDEX_CATALOG_ID,
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.ok:
        return response.json()['translations'][0]['text']
    return 'Ошибка перевода'


def send_message(chat_id, text):
    url = URL + 'sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(url, json=payload)


def handle_updates():
    last_update_id = None
    translating = {}

    while True:
        # обновления от Telegram
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

            if text == '/start':
                send_message(chat_id, "Привет! Я бот для перевода текста. Напишите /translate для начала работы.")
                translating[chat_id] = False

            elif text == '/translate':
                send_message(chat_id, "Режим перевода активирован. Отправьте текст, и я переведу его на английский.")
                translating[chat_id] = True

            elif text == '/stop':
                send_message(chat_id, "Режим перевода завершен. Чтобы снова активировать перевод, отправьте /translate.")
                translating[chat_id] = False

            elif translating.get(chat_id):
                translated_text = translate_text(text)
                send_message(chat_id, f"Перевод:\n{translated_text}")

            else:
                send_message(chat_id, "Чтобы перевести текст, активируйте режим перевода командой /translate.")

        time.sleep(1)

if __name__ == '__main__':
    handle_updates()
