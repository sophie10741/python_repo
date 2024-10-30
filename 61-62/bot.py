import telebot
import random

token = ''
bot = telebot.TeleBot(token)

# состояние игры для каждого пользователя
user_in_game = {}  # {user_id: True/False}
bot_numbers = {}  # {user_id: загаданный номер}


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот для игры в угадывание чисел. Введи команду /game, чтобы начать игру.")


@bot.message_handler(commands=['game'])
def game(message):
    user_id = message.from_user.id
    bot_number = random.randint(1, 100)

    user_in_game[user_id] = True  # пользователь в игре
    bot_numbers[user_id] = bot_number  # загаданное число

    bot.reply_to(message, "Я загадал число от 1 до 100. Попробуй угадать его!")


@bot.message_handler(func=lambda message: True)
def guess(message):
    user_id = message.from_user.id

    # проверка, что пользователь в игре
    if user_in_game.get(user_id):
        try:
            user_guess = int(message.text)
            bot_number = bot_numbers[user_id]

            # угадал ли пользователь
            if user_guess == bot_number:
                bot.reply_to(message, "Угадал!")
                user_in_game[user_id] = False  # игра завершена
            else:
                bot.reply_to(message, "Не угадал, попробуй еще раз!")
        except ValueError:
            # сообщение о неправильном формате, если введен текст, а не число
            bot.reply_to(message, "Пожалуйста, введи число.")
    else:
        # бот не отвечает, если пользователь не начал игру
        pass


# запуск
bot.infinity_polling()
