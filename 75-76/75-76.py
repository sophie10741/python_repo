import sqlite3

def initialize_database():
    connection = sqlite3.connect('notes.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS note (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            rating INTEGER CHECK(rating >= 1 AND rating <= 5)
        )
    ''')
    connection.commit()
    connection.close()

def add_note(name, rating):
    connection = sqlite3.connect('notes.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO note (name, rating) VALUES (?, ?)', (name, rating))
    connection.commit()
    connection.close()


def get_notes():
    connection = sqlite3.connect('notes.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM note')
    rows = cursor.fetchall()
    connection.close()
    return rows

def get_popular_notes():
    connection = sqlite3.connect('notes.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM note WHERE rating > 3')
    rows = cursor.fetchall()
    connection.close()
    return rows

def main():
    initialize_database()

    while True:
        print("\nЧто хотите сделать?")
        print("1 - Добавить заметку")
        print("2 - Прочитать все заметки")
        print("3 - Вывести популярные заметки")
        print("q - Выход")

        choice = input("Введите номер действия: ").strip()

        if choice == '1':
            name = input("Введите название заметки: ")
            while True:
                try:
                    rating = int(input("Введите рейтинг заметки (1-5): "))
                    if 1 <= rating <= 5:
                        break
                    else:
                        print("Рейтинг должен быть от 1 до 5!")
                except ValueError:
                    print("Введите число от 1 до 5.")
            add_note(name, rating)
            print("Заметка добавлена!")
        elif choice == '2':
            notes = get_notes()
            if notes:
                print("\nВсе заметки:")
                for note in notes:
                    print(f"{note[0]}. {note[1]} - Рейтинг: {note[2]}")
            else:
                print("\nНет заметок!")
        elif choice == '3':
            popular_notes = get_popular_notes()
            if popular_notes:
                print("\nПопулярные заметки:")
                for note in popular_notes:
                    print(f"{note[0]}. {note[1]} - Рейтинг: {note[2]}")
            else:
                print("\nНет популярных заметок!")
        elif choice == 'q':
            print("До свидания!")
            break
        else:
            print("Неверный ввод. Попробуйте снова.")


if __name__ == "__main__":
    main()
