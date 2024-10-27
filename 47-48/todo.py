class TasksModel:
    """Модель данных"""
    def __init__(self):
        self.tasks = [{'name': 'поспать', 'status': 'в ожидании'}]

    def get_tasks(self):
        """Получить все задачи"""
        return self.tasks

    def add_task(self, name):
        task = {'name': name, 'status': 'в ожидании'}
        self.tasks.append(task)

    def complete_task(self, task_number):
        self.tasks[task_number]['status'] = 'Выполнена'

    def delete_task(self, task_number):
        self.tasks.pop(task_number)

class View:

    @staticmethod
    def show_all_tasks(tasks):
        """Выводим список всех задач"""
        for number, task in enumerate(tasks, 1):
            print(f"{number}. {task['name']} : {task['status']}")

    @staticmethod
    def show_add_task():
        return input('Введи название задачи: ')

    @staticmethod
    def show_complete_task():
        return int(input('Введи номер задачи: '))

    @staticmethod
    def show_delete_task():
        return int(input('Введи номер задачи: '))

class Controller:
    """Класс для бизнес логики.
    Взаимодействует с моделью и представлением
    """
    def __init__(self, view, model):
        self.view = view
        self.model = model

    def add_task(self):
        """Добавление задачи"""
        tasks = self.model.get_tasks()
        self.view.show_all_tasks(tasks)
        task_name = self.view.show_add_task()
        self.model.add_task(task_name)
        self.view.show_all_tasks(tasks)

    def show_tasks(self):
        """Просмотр всех задач"""
        tasks = self.model.get_tasks()
        self.view.show_all_tasks(tasks)

    def complete_task(self):
        """Выполнить задачу"""

        task_number = self.view.show_complete_task() # спросили номер задачи
        task_number -= 1

        self.model.complete_task(task_number) # изменить статус

    def delete_task(self):
        """Удаление задачи"""
        tasks = self.model.get_tasks()

        self.view.show_all_tasks(tasks)
        task_number = self.view.show_delete_task()  # спросили номер задачи
        task_number -= 1
        self.model.delete_task(task_number)
        self.view.show_all_tasks(tasks)

# инициализируем объекты MVC
model = TasksModel() # Модель
view = View()  # Представление
contr = Controller(view, model)  # Контроллер

while True:
    print("1 - Добавить задачу")
    print("2 - Выполнить задачу")
    print("3 - Посмотреть список задач")
    print("4 - удалить задачу")
    print("5 - Выйти")

    choice = input('Что ты хочешь сделать: ')

    if choice == '1':
        contr.add_task()
    elif choice == '2':
        contr.complete_task()
    elif choice == '3':
        print('Вот ваши задачи:')
        contr.show_tasks()
    elif choice == '4':
        contr.delete_task()
    elif choice == '5':
        print("До свидания!")
        break