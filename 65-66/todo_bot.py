import telebot
from telebot import types
import json


class TaskModel:
    def __init__(self, filename):
        self.filename = filename
        self.tasks = self._load_from_file()

    def get_tasks(self):
        return self.tasks

    def add_task(self, task):
        """Добавили метод"""
        self.tasks.append(task)
        self._save_to_file()

    def _load_from_file(self):
        with open(self.filename, 'r', encoding='utf-8') as f:
            tasks = json.load(f)
        return tasks

    def _save_to_file(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f)


token = ''
bot = telebot.TeleBot(token)

user_state = ''
ADD_STATE = 'add'


db = TaskModel('tasks.json')


@bot.message_handler(commands=["start"])
def start(message):
    description = 'Я бот для создания списка дел. Жми кнопку или команду /add для добавления'

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('добавить задачу')
    button2 = types.KeyboardButton('посмотреть задачи')
    markup.add(button)
    markup.add(button2)

    bot.send_message(message.chat.id, description, reply_markup=markup)


@bot.message_handler(regexp='добавить задачу')
@bot.message_handler(commands=["add"])
def add(message):
    global user_state
    user_state = ADD_STATE
    bot.reply_to(message, 'Введи текст задачи: ')


@bot.message_handler(regexp='посмотреть задачи')
@bot.message_handler(commands=["tasks"])
def get_task_list(message):
    tasks = db.get_tasks()
    bot.reply_to(message, "\n".join(tasks))


@bot.message_handler(commands=["end"])
def end_state(message):
    global user_state
    user_state = ''
    bot.reply_to(message, "Мы вышли из сеанса добавленя задачи")


@bot.message_handler(commands=["keyboard"])
def keyboard(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('добавить задачу')
    markup.add(button)

    bot.send_message(message.chat.id, 'Какой-то текст', reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def get_task(message):
    global user_state
    if user_state == ADD_STATE:
        db.add_task(message.text)
        user_state = ''
        bot.reply_to(message, 'Добавил в базу')


bot.infinity_polling()