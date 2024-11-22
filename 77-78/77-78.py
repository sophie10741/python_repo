import sqlite3


def initialize_database():
    connection = sqlite3.connect('notes.db')
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS note (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            rating INTEGER CHECK(rating >= 1 AND rating <= 5),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    connection.commit()
    connection.close()

def register_user(username, password):
    try:
        connection = sqlite3.connect('notes.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        connection.commit()
        connection.close()
        print("Регистрация прошла успешно!")
    except sqlite3.IntegrityError:
        print("Пользователь с таким именем уже существует!")


def authenticate_user(username, password):
    connection = sqlite3.connect('notes.db')
    cursor = connection.cursor()
    cursor.execute('SELECT id FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    connection.close()
    if user:
        print("Авторизация успешна!")
        return user[0]
    else:
        print("Неверный логин или пароль.")
        return None


def add_note(user_id, name, rating):
    connection = sqlite3.connect('notes.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO note (user_id, name, rating) VALUES (?, ?, ?)', (user_id, name, rating))
    connection.commit()
    connection.close()


def get_notes(user_id):
    connection = sqlite3.connect('notes.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM note WHERE user_id = ?', (user_id,))
    rows = cursor.fetchall()
    connection.close()
    return rows


def get_popular_notes(user_id):
    connection = sqlite3.connect('notes.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM note WHERE user_id = ? AND rating > 3', (user_id,))
    rows = cursor.fetchall()
    connection.close()
    return rows


def main():
    initialize_database()

    print("Добро пожаловать!")
    print("1 - Зарегистрироваться")
    print("2 - Войти")

    user_id = None
    choice = input("Выберите действие: ").strip()

    if choice == '1':
        username = input("Введите имя пользователя: ")
        password = input("Введите пароль: ")
        register_user(username, password)
    elif choice == '2':
        username = input("Введите имя пользователя: ")
        password = input("Введите пароль: ")
        user_id = authenticate_user(username, password)

    if not user_id:
        return

    while True:
        print("\nЧто хотите сделать?")
        print("1 - Добавить заметку")
        print("2 - Прочитать все заметки")
        print("3 - Вывести популярные заметки")
        print("q - Выход")

        action = input("Введите номер действия: ").strip()

        if action == '1':
            name = input("Введите название заметки: ")
            while True:
                try:
                    rating = int(input("Введите рейтинг заметки (1-5): "))
                    if 1 <= rating <= 5:
                        break
                    else:
                        print("Рейтинг должен быть от 1 до 5!")
                except ValueError:
                    print("Пожалуйста, введите число от 1 до 5.")
            add_note(user_id, name, rating)
            print("Заметка добавлена!")
        elif action == '2':
            notes = get_notes(user_id)
            if notes:
                print("\nВаши заметки:")
                for note in notes:
                    print(f"{note[0]}. {note[2]} - Рейтинг: {note[3]}")
            else:
                print("\nУ вас нет заметок!")
        elif action == '3':
            popular_notes = get_popular_notes(user_id)
            if popular_notes:
                print("\nПопулярные заметки:")
                for note in popular_notes:
                    print(f"{note[0]}. {note[2]} - Рейтинг: {note[3]}")
            else:
                print("\nНет популярных заметок!")
        elif action == 'q':
            print("До свидания!")
            break
        else:
            print("Неверный ввод. Попробуйте снова.")


if __name__ == "__main__":
    main()
