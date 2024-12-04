import sqlite3
import telebot
from telebot import types


# для работы с базой данных
class TaskModelSQL:
    def __init__(self, db_name):
        self.db_name = db_name

    def get_tasks(self, user_id):
        connection = sqlite3.connect(self.db_name)
        connection.row_factory = self._dict_factory

        cursor = connection.cursor()
        rows = cursor.execute('SELECT * FROM task WHERE user_id = ?', (user_id,)).fetchall()
        connection.close()
        return rows

    def add_task(self, text, user_id):
        connection = sqlite3.connect(self.db_name)
        connection.row_factory = self._dict_factory

        cursor = connection.cursor()
        cursor.execute('INSERT INTO task (name, user_id) VALUES (?, ?)', (text, user_id))
        connection.commit()
        connection.close()

    def get_user(self, telegram_id):
        connection = sqlite3.connect(self.db_name)
        connection.row_factory = self._dict_factory

        cursor = connection.cursor()
        rows = cursor.execute('SELECT * FROM user WHERE telegram_id = ?', (telegram_id,)).fetchone()
        connection.close()
        return rows

    def add_user(self, telegram_id):
        connection = sqlite3.connect(self.db_name)
        connection.row_factory = self._dict_factory

        cursor = connection.cursor()
        cursor.execute('INSERT INTO user (telegram_id) VALUES (?)', (telegram_id,))
        connection.commit()
        connection.close()

    def delete_task(self, task_id, user_id):
        """Удаляет задачу по её ID и ID пользователя"""
        connection = sqlite3.connect(self.db_name)
        connection.row_factory = self._dict_factory

        cursor = connection.cursor()
        cursor.execute('DELETE FROM task WHERE id = ? AND user_id = ?', (task_id, user_id))
        connection.commit()
        connection.close()

    @staticmethod
    def _dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d


# Инициализация бота
token = ''
bot = telebot.TeleBot(token)

# Переменные состояния
user_state = ''
ADD_STATE = 'add'

# Путь к базе данных
db_name = 'bot_todo.db'
db = TaskModelSQL(db_name)


# Команда /start
@bot.message_handler(commands=["start"])
def start(message):
    description = 'Я бот для создания списка дел. Используйте команды: /add, /tasks, /delete <ID>'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("добавить задачу", "посмотреть задачи")

    telegram_id = message.chat.id
    user = db.get_user(telegram_id)
    if not user:
        db.add_user(telegram_id)
        bot.reply_to(message, 'Вы добавлены в базу.')

    bot.send_message(message.chat.id, description, reply_markup=markup)


# Команда /add или "добавить задачу"
@bot.message_handler(commands=["add"])
@bot.message_handler(regexp="добавить задачу")
def add(message):
    global user_state
    user_state = ADD_STATE
    bot.reply_to(message, 'Введите текст задачи: ')


# Команда /tasks или "посмотреть задачи"
@bot.message_handler(commands=["tasks"])
@bot.message_handler(regexp="посмотреть задачи")
def get_task_list(message):
    telegram_id = message.chat.id
    user = db.get_user(telegram_id)
    if not user:
        return bot.reply_to(message, 'Вас нет в базе.')

    tasks = db.get_tasks(user['id'])
    if not tasks:
        return bot.reply_to(message, 'У вас нет задач.')

    tasks_string = '\n'.join([f"{task['name']} ({task['id']})" for task in tasks])
    bot.reply_to(message, tasks_string)


# Команда /delete <ID>
@bot.message_handler(commands=["delete"])
def delete_task(message):
    try:
        # ID из команды
        parts = message.text.split()
        if len(parts) != 2 or not parts[1].isdigit():
            return bot.reply_to(message, "Пожалуйста, укажите корректный ID задачи. Пример: /delete 3")

        task_id = int(parts[1])
        telegram_id = message.chat.id

        # есть ли пользователь в базе
        user = db.get_user(telegram_id)
        if not user:
            return bot.reply_to(message, "Вас нет в базе данных!")

        # удалить задачу
        db.delete_task(task_id, user['id'])
        bot.reply_to(message, f"Задача с ID {task_id} удалена.")
    except Exception as e:
        bot.reply_to(message, f"Ошибка при удалении задачи: {e}")



# Обработка сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global user_state
    telegram_id = message.chat.id
    user = db.get_user(telegram_id)
    if user_state == ADD_STATE:
        db.add_task(message.text, user['id'])
        user_state = ''
        bot.reply_to(message, 'Задача добавлена в базу.')



# Запуск бота
bot.infinity_polling()
