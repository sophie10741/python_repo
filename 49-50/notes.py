import tkinter as tk
import json

from abc import ABC, abstractmethod


class NoteModel:
    """База данных для хранения заметок"""

    def __init__(self):
        self._notes = self._load_from_file()

    def get_notes(self):
        return self._notes

    def add_note(self, text):
        """Добавление новой заметки"""
        next_id = self._get_last_id() + 1  # получаем новый id
        note = {"id": next_id, "text": text}  # создаем заметку
        self._notes.append(note)  # добавляем в список

        self.save_to_file()

    def delete_by_id(self, note_id):
        """Удаление по id"""
        for number, note in enumerate(self._notes):
            if note['id'] == note_id:
                self._notes.pop(number)
                break
        else:
            print('Такой заметки нет')

    def find_by_text(self, text):
        """Поиск заметки"""
        res_notes = []
        for note in self._notes:
            if text in note['text']:
                res_notes.append(note)
        return res_notes

    def _load_from_file(self):
        """Загрузка данных из файла"""
        with open('notes.json', 'r', encoding='utf-8') as f:
            notes = json.load(f)
        return notes

    def save_to_file(self):
        with open('notes.json', 'w', encoding='utf-8') as f:
            notes = json.dump(self._notes, f)
        return notes

    def _get_last_id(self):
        """Поиск максимального id"""
        if self._notes:
            max = self._notes[0]['id']
            for note in self._notes:
                if note['id'] > max:
                    max = note['id']
        else:
            max = 0
        return max


class AbstractView(ABC):
    """Абстрактный класс для реализации классов-представлений"""

    @abstractmethod
    def render_notes(self, notes):
        """Абстрактный метод для визуализации заметок"""
        pass



class GraphicView(AbstractView):

    def render_notes(self, notes):
        """Показывает заметки в окне"""
        self._create_window()

        # self.listbox.delete(0, 'end')
        for note in notes:
            text = f"{note['id']} --- {note['text']}"
            self.listbox.insert(tk.END, text)
        self.root.mainloop()

    def _create_window(self):
        self.root = tk.Tk()
        self.root.title("Тестовое окошко")
        self.listbox = tk.Listbox(self.root, height=10, width=50)
        self.listbox.pack(padx=10, pady=10)



class ConsoleView(AbstractView):

    def render_notes(self, notes):
        for note in notes:
            text = f"{note['id']} --- {note['text']}"
            print(text)


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def show_notes(self):
        """Показать все заметки на экране"""
        notes = self.model.get_notes()
        self.view.render_notes(notes)

    def add_note(self):
        text = input('Введи текст заметки: ')
        self.model.add_note(text)

    def delete_note(self):
        self.show_notes()
        note_id = int(input('Введи id заметки: '))
        self.model.delete_by_id(note_id)

    def find_note(self):
        text = input('Введи текст для поиска: ')
        notes = self.model.find_by_text(text)
        self.view.render_notes(notes)


model = NoteModel()

graphic_view = GraphicView()
console_view = ConsoleView()

contr = Controller(model, graphic_view)

while True:
    print('\n\n1 - Посмотреть все заметки')
    print('2 - Добавить заметку')
    print('3 - Удалять заметку')
    print('4 - Найти заметку')
    print('q - Выйти')

    choice = input("Выбирай: ")

    if choice == '1':
        contr.show_notes()
    elif choice == '2':
        contr.add_note()
    elif choice == '3':
        contr.delete_note()
    elif choice == '4':
        contr.find_note()
    elif choice == 'q':
        break