class Shop:
    def __init__(self):
        self.products = {'яблоко': 200, 'манго': 100}
        self.check = 0

    def buy_product(self, name):
        try:
            # Проверяем, есть ли товар в списке
            if name not in self.products:
                raise ValueError(f"Товар '{name}' отсутствует в списке.")
            self.check += self.products[name]
            print(f'Купили товар {name}')
        except ValueError as e:
            print(e)

    def add_product(self, name, price):
        try:
            # Проверка на длину названия
            if len(name) < 3:
                raise ValueError("Название товара должно содержать не менее трех букв.")
            # Проверка на отрицательную цену
            if price < 0:
                raise ValueError("Цена товара не может быть отрицательной.")
            self.products.update({name: price})
            print(f'Добавили товар {name} по цене {price}')
        except ValueError as e:
            print(e)


shop = Shop()

while True:
    print('Что вы хотите сделать: ')
    print('1 - купить товар')
    print('2 - добавить товар')
    ans = input('Выберите: ')

    if ans == '1':
        name = input('Введите название товара: ')
        shop.buy_product(name)

    elif ans == '2':
        name = input('Введите название товара: ')
        try:
            price = int(input('Введите цену товара: '))
            shop.add_product(name, price)
        except ValueError:
            print("Ошибка: введите числовое значение для цены товара.")
