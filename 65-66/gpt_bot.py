import requests
import telebot
from telebot import types

class YandexGPT:
    def __init__(self, token, catalog):
        self.token = token
        self.catalog = catalog

    def send_request(self, question):
        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        prompt = {
            "modelUri": f'gpt://{self.catalog}/yandexgpt-lite',
            "completionOptions": {
                "stream": False,
                "temperature": 0.6,
                "maxTokens": 200
            },
            "messages" : [
                {
                    "role": "user",
                    "text": f"{question}"
                }
            ]
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {self.token}"
        }

        response = requests.post(url, headers=headers, json=prompt)
        text = response.json()['result']['alternatives'][0]['message']['text']
        return text
token = '7601813298:AAEcYq2v4qWQdAx3zyp4nckFwp65WmX1tp8'
bot = telebot.TeleBot(token)

user_state = ''
DIALOG_STATE = 'dialog'

y_token = 'AQVNzs9wZZIs12ImlgJGaaSmb9myFjW-KjB45GtU'
y_catalog = 'b1gtphdg2vndncqf33o7'

yandex_bot = YandexGPT(y_token, y_catalog)

users = {}

@bot.message_handler(commands=["start"])
def start(message):
    description = 'Я бот - нейросеть. Жми на кнопку или вводи команду /ask чтобы задать вопрос'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('задать вопрос')
    markup.add(button)

    users[message.chat.id] = {'count': 0}
    print(users)

    bot.send_message(message.chat.id, description, reply_markup=markup)



@bot.message_handler(commands=["ask"])
@bot.message_handler(regexp='задать вопрос')
def ask(message):
    global user_state
    user_state = DIALOG_STATE
    bot.reply_to(message, 'Диалог начат. Чтобы выйти - жми команду /end')

@bot.message_handler(commands=["end"])
def end(message):
    global user_state
    user_state = ''
    bot.reply_to(message, 'Пока!')
@bot.message_handler(func=lambda message: True)
def get_question(message):
    if user_state == DIALOG_STATE:

        chat_id = message.chat.id
        if chat_id in users:
            if users[chat_id]['count'] < 4:
                response = yandex_bot.send_request(message.text)
                users[chat_id]['count'] += 1
                bot.reply_to(message, response)
            else:
                bot.reply_to(message,'Плати деньги.')
    print(users)

bot.infinity_polling()