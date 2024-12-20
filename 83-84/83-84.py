import sqlite3
import telebot
from sqlalchemy import create_engine, text
from telebot import types

class TaskModelSQLAlchemy:
    def __init__(self, db_name):
        self.engine = create_engine(f'sqlite:///{db_name}')

    def get_tasks(self, user_id):
        with self.engine.connect() as con:
            res = con.execute(text('select * from task where user_id = :user_id'),
                              {'user_id': user_id}).mappings().all()
            return res

    def get_user(self, telegram_id):
        with self.engine.connect() as con:
            r = con.execute(text('select * from user where telegram_id = :telegram_id'),
                        {'telegram_id': telegram_id}).mappings().one_or_none()
            return r

    def add_user(self, telegram_id):
        with self.engine.connect() as con:
            con.execute(text('insert into user (telegram_id) values(:telegram_id)'),
                             {'telegram_id': telegram_id})
            con.commit()

    def add_task(self, name, user_id):
        with self.engine.connect() as con:
            con.execute(text('insert into task (user_id, name, status) values(:user_id, :name, "запланирована")'),
                        {'user_id': user_id, 'name': name})
            con.commit()

    def delete_task(self, task_id, user_id):
        with self.engine.connect() as con:
            con.execute(text('delete from task where id=:task_id and user_id = :user_id'),
                        {'task_id': task_id, 'user_id': user_id})
            con.commit()

    def update_task_status(self, task_id, user_id, status):
        with self.engine.connect() as con:
            con.execute(text('update task set status=:status where id=:task_id and user_id = :user_id'),
                        {'task_id': task_id, 'user_id': user_id, 'status': status})
            con.commit()

token = ''
bot = telebot.TeleBot(token)

user_state = ''
ADD_STATE = 'add'
DEL_STATE = 'del'
STATUS_STATE = 'status'

db_name = 'bot_todo.db'
db = TaskModelSQLAlchemy(db_name)

@bot.message_handler(commands=["start"])
def start(message):
    description = 'Я бот для создания списка дел. Используй команды или кнопки для работы с задачами.'

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_add = types.KeyboardButton('Добавить задачу')
    button_view = types.KeyboardButton('Посмотреть задачи')
    button_change_status = types.KeyboardButton('Изменить статус задачи')
    button_delete = types.KeyboardButton('Удалить задачу')
    markup.add(button_add, button_view)
    markup.add(button_change_status, button_delete)

    telegram_id = message.chat.id
    user = db.get_user(telegram_id)
    if not user:
        db.add_user(telegram_id)
        bot.reply_to(message, 'Я вас добавил в базу.')

    bot.send_message(message.chat.id, description, reply_markup=markup)

@bot.message_handler(regexp='Добавить задачу')
@bot.message_handler(commands=["add"])
def add(message):
    global user_state
    user_state = ADD_STATE
    bot.reply_to(message, 'Введите текст задачи:')

@bot.message_handler(regexp='Удалить задачу')
@bot.message_handler(commands=["del"])
def delete(message):
    global user_state
    user_state = DEL_STATE

    telegram_id = message.chat.id
    user = db.get_user(telegram_id)
    tasks = db.get_tasks(user['id'])
    if not tasks:
        return bot.reply_to(message, 'У вас нет задач для удаления.')

    tasks_str = 'Выберите задачу для удаления (введите номер):\n\n'
    for number, task in enumerate(tasks, 1):
        tasks_str += f'{number}. {task["name"]} ({task["status"]})\n'
    bot.reply_to(message, tasks_str)

@bot.message_handler(regexp='Посмотреть задачи')
@bot.message_handler(commands=["tasks"])
def get_task_list(message):
    telegram_id = message.chat.id
    user = db.get_user(telegram_id)
    if not user:
        return bot.reply_to(message, 'Вас нет в базе.')
    tasks = db.get_tasks(user['id'])
    if not tasks:
        return bot.reply_to(message, 'У вас нет задач.')
    tasks_str = '\n'.join([f'{i+1}. {task["name"]} ({task["status"]})' for i, task in enumerate(tasks)])
    bot.reply_to(message, tasks_str)

@bot.message_handler(regexp='Изменить статус задачи')
@bot.message_handler(commands=["status"])
def change_status(message):
    global user_state
    user_state = STATUS_STATE

    telegram_id = message.chat.id
    user = db.get_user(telegram_id)
    tasks = db.get_tasks(user['id'])
    if not tasks:
        return bot.reply_to(message, 'У вас нет задач для изменения статуса.')

    tasks_str = 'Выберите задачу для изменения статуса (введите номер):\n\n'
    for number, task in enumerate(tasks, 1):
        tasks_str += f'{number}. {task["name"]} ({task["status"]})\n'
    bot.reply_to(message, tasks_str)

@bot.message_handler(func=lambda message: True)
def handle_input(message):
    global user_state
    telegram_id = message.chat.id
    user = db.get_user(telegram_id)

    if user_state == ADD_STATE:
        db.add_task(message.text, user['id'])
        user_state = ''
        bot.reply_to(message, 'Задача добавлена.')

    elif user_state == DEL_STATE:
        try:
            task_number = int(message.text)
        except ValueError:
            return bot.reply_to(message, 'Ошибка! Введите номер задачи.')

        tasks = db.get_tasks(user['id'])
        if 0 < task_number <= len(tasks):
            task = tasks[task_number - 1]
            db.delete_task(task['id'], user['id'])
            bot.reply_to(message, 'Задача удалена.')
        else:
            bot.reply_to(message, 'Такой задачи нет.')
        user_state = ''

    elif user_state == STATUS_STATE:
        try:
            task_number = int(message.text)
        except ValueError:
            return bot.reply_to(message, 'Ошибка! Введите номер задачи.')

        tasks = db.get_tasks(user['id'])
        if 0 < task_number <= len(tasks):
            task = tasks[task_number - 1]
            bot.reply_to(message, f'Введите новый статус для задачи "{task["name"]}":')
            user_state = f'status_{task["id"]}'
        else:
            bot.reply_to(message, 'Такой задачи нет.')

    elif user_state.startswith('status_'):
        task_id = int(user_state.split('_')[1])
        db.update_task_status(task_id, user['id'], message.text)
        bot.reply_to(message, 'Статус задачи обновлён.')
        user_state = ''

bot.infinity_polling()
