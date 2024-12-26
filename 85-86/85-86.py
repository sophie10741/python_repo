import telebot
from telebot import types
from sqlalchemy import create_engine, select, delete, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship
from typing import List


# ORM модели
class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int]
    tasks: Mapped[List["Task"]] = relationship(back_populates="user")


class Task(Base):
    __tablename__ = 'task'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    status: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped["User"] = relationship(back_populates="tasks")

# взаимодействие с бд
class TaskModelORM:
    def __init__(self, db_name):
        self.engine = create_engine(f'sqlite:///{db_name}')
        Base.metadata.create_all(self.engine)

    def get_user(self, telegram_id):
        with Session(self.engine) as session:
            return session.scalars(select(User).where(User.telegram_id == telegram_id)).one_or_none()

    def add_user(self, telegram_id):
        with Session(self.engine) as session:
            user = User(telegram_id=telegram_id)
            session.add(user)
            session.commit()

    def get_tasks(self, user_id):
        with Session(self.engine) as session:
            return session.scalars(select(Task).where(Task.user_id == user_id)).all()

    def add_task(self, name, user_id):
        with Session(self.engine) as session:
            task = Task(name=name, status="запланирована", user_id=user_id)
            session.add(task)
            session.commit()

    def delete_task(self, task_id):
        with Session(self.engine) as session:
            session.execute(delete(Task).where(Task.id == task_id))
            session.commit()

    def update_task_status(self, task_id, status):
        with Session(self.engine) as session:
            task = session.get(Task, task_id)
            if task:
                task.status = status
                session.commit()


# Бот
token = ''
bot = telebot.TeleBot(token)

db = TaskModelORM('bot_todo.db')

user_state = ''
ADD_STATE = 'add'
DEL_STATE = 'del'
STATUS_STATE = 'status'


@bot.message_handler(commands=["start"])
def start(message):
    description = 'Я бот для списка дел. Используйте кнопки для работы с задачами.'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Добавить задачу", "Посмотреть задачи", "Изменить статус", "Удалить задачу")

    telegram_id = message.chat.id
    if not db.get_user(telegram_id):
        db.add_user(telegram_id)
        bot.reply_to(message, "Вы добавлены в базу.")

    bot.send_message(message.chat.id, description, reply_markup=markup)


@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    global user_state
    telegram_id = message.chat.id
    user = db.get_user(telegram_id)
    if not user:
        return bot.reply_to(message, "Вы не зарегистрированы. Используйте /start.")

    if message.text == "Добавить задачу":
        user_state = ADD_STATE
        bot.reply_to(message, "Введите текст задачи:")
    elif message.text == "Посмотреть задачи":
        tasks = db.get_tasks(user.id)
        if tasks:
            response = "\n".join([f"{i + 1}. {task.name} ({task.status})" for i, task in enumerate(tasks)])
        else:
            response = "Нет задач."
        bot.reply_to(message, response)
    elif message.text == "Удалить задачу":
        user_state = DEL_STATE
        tasks = db.get_tasks(user.id)
        if tasks:
            response = "Введите номер задачи для удаления:\n" + "\n".join(
                [f"{i + 1}. {task.name}" for i, task in enumerate(tasks)]
            )
        else:
            response = "Нет задач для удаления."
        bot.reply_to(message, response)
    elif message.text == "Изменить статус":
        user_state = STATUS_STATE
        tasks = db.get_tasks(user.id)
        if tasks:
            response = "Введите номер задачи для изменения статуса:\n" + "\n".join(
                [f"{i + 1}. {task.name} ({task.status})" for i, task in enumerate(tasks)]
            )
        else:
            response = "Нет задач для изменения статуса."
        bot.reply_to(message, response)
    elif user_state == ADD_STATE:
        db.add_task(message.text, user.id)
        user_state = ''
        bot.reply_to(message, "Задача добавлена.")
    elif user_state == DEL_STATE:
        try:
            task_number = int(message.text) - 1
            tasks = db.get_tasks(user.id)
            if 0 <= task_number < len(tasks):
                db.delete_task(tasks[task_number].id)
                bot.reply_to(message, "Задача удалена.")
            else:
                bot.reply_to(message, "Неверный номер задачи.")
        except ValueError:
            bot.reply_to(message, "Введите корректный номер задачи.")
        user_state = ''
    elif user_state == STATUS_STATE:
        try:
            task_number = int(message.text) - 1
            tasks = db.get_tasks(user.id)
            if 0 <= task_number < len(tasks):
                bot.reply_to(message, "Введите новый статус задачи:")
                user_state = f"status_{tasks[task_number].id}"
            else:
                bot.reply_to(message, "Неверный номер задачи.")
        except ValueError:
            bot.reply_to(message, "Введите корректный номер задачи.")
    elif user_state.startswith("status_"):
        task_id = int(user_state.split("_")[1])
        db.update_task_status(task_id, message.text)
        bot.reply_to(message, "Статус задачи обновлен.")
        user_state = ''


bot.infinity_polling()
