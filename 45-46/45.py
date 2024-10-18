class Shop:
    def __init__(self, products=None):
        if products is None:
            self.products = {"Молоко": 10, "Колбаса": 20}
        else:
            self.products = products
        self.total_sum = 0
        self.receipts = 0
        self.history = []

    def display_products(self):
        print("Доступные продукты:")
        for product, price in self.products.items():
            print(f"{product}: {price} руб.")
        print()

    def buy(self, product_name):
        if product_name in self.products:
            price = self.products[product_name]
            self.total_sum += price
            self._check_discount(product_name)
            self.receipts += 1
            self.history.append(product_name)
            print(f"Купили {product_name}")
        else:
            print(f"Такого продукта нет в наличии. Попробуйте другой.")

    def add_product(self, product_name, price):
        self.products[product_name] = price
        print(f"Продукт {product_name} добавлен с ценой {price} руб.")

    def delete_product(self, product_name):
        if product_name in self.products:
            del self.products[product_name]
            print(f"{product_name} удален из списка продуктов.")
        else:
            print(f"{product_name} отсутствует в списке продуктов.")

    def get_info(self):
        print(f"Общая сумма покупок: {self.total_sum} руб.")
        print(f"Чеков: {self.receipts}")
        print("История покупок:", ", ".join(self.purchase_history))

    def _check_discount(self, product_name):
        if product_name in {'Молоко', 'Яйца'}:
            self.total_sum -= 5
            print(f"На {product_name} применена скидка 5 руб.!")

    def show_menu(self):
        """Интерфейс команд для пользователя."""
        print("\n--- Меню магазина ---")
        print("1: Просмотреть товары")
        print("2: Купить продукт")
        print("3: Добавить продукт")
        print("4: Удалить продукт")
        print("5: Информация о покупках")
        print("0: Выйти")
        print("---------------------\n")

    def run(self):
        while True:
            self.show_menu()
            choice = input("Выберите действие: ")

            if choice == "1":
                self.display_products()
            elif choice == "2":
                product = input("Введите название продукта для покупки: ")
                self.buy(product)
            elif choice == "3":
                product = input("Введите название продукта: ")
                price = int(input(f"Введите цену для {product}: "))
                self.add_product(product, price)
            elif choice == "4":
                product = input("Введите название продукта для удаления: ")
                self.delete_product(product)
            elif choice == "5":
                self.get_info()
            elif choice == "0":
                print("Спасибо за покупки! До свидания!")
                break
            else:
                print("Некорректный ввод. Попробуйте снова.")


shop = Shop()
shop.run()
