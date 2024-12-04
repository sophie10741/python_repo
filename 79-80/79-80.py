import sqlite3
import tkinter as tk


class Authenticator:
    """Класс для управления аутентификацией."""

    def __init__(self, password):
        self.password = password

    def authenticate(self):
        """Проверяет пароль пользователя."""
        user_password = input("Введите пароль: ").strip()
        if user_password == self.password:
            print("Авторизация успешна!")
            return True
        else:
            print("Неверный пароль. Доступ запрещен.")
            return False


class NoteModelSQL:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.connection.row_factory = self._dict_factory

    def get_notes(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM notes")
        return cursor.fetchall()

    def add_note(self, text):
        with self.connection as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO notes (text) VALUES (?)", (text,))

    @staticmethod
    def _dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def __del__(self):
        print("Закрытие подключения")
        self.connection.close()


class NoteWindow:
    def __init__(self, model):
        self.model = model
        self.create_window()
        self.show_notes()
        self.root.mainloop()

    def create_window(self):
        self.root = tk.Tk()
        self.root.title("Заметки")

        # Окошко для ввода
        self.input = tk.Text(self.root, height=10, width=20)
        self.input.grid(row=0, column=0, padx=10, pady=10)

        # Окошко для вывода
        self.output = tk.Listbox(self.root, height=10, width=20)
        self.output.grid(row=0, column=1, padx=10, pady=10)

        self.button = tk.Button(self.root, text="Добавить заметку", command=self.add_note)
        self.button.grid(row=1, column=0, padx=10, pady=10)

    def show_notes(self):
        notes = self.model.get_notes()
        self.output.delete(0, tk.END)
        for note in notes:
            self.output.insert(tk.END, note["text"])

    def add_note(self):
        text = self.input.get("1.0", tk.END).strip()
        self.model.add_note(text)
        self.show_notes()
        self.input.delete("1.0", tk.END)


# Авторизация
authenticator = Authenticator(password="1234")
if authenticator.authenticate():
    sql_model = NoteModelSQL("notes.db")
    NoteWindow(sql_model)
else:
    print("Программа завершена.")
