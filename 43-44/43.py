import random
class Car:
    def __init__(self, color, fuel, fuel_count_100):
        self.color = color
        self.fuel = fuel
        self.fuel_count_100 = fuel_count_100
        self.mileage = 0

    def drive(self, km):
        fuel_needed = (km / 100) * self.fuel_count_100
        if fuel_needed <= self.fuel:
            self.fuel -= fuel_needed
            self.mileage += km
            print(f"Мы проехали {km} км.")
        else:
            print("Не хватает топлива.")

    def get_mileage(self):
        return self.mileage

class SportCar(Car):
    def fast_drive(self, km):
        fuel_needed = (km / 100) * (self.fuel_count_100 * 1.5)
        if fuel_needed <= self.fuel:
            self.fuel -= fuel_needed
            self.mileage += km
            print(f"Мы проехали {km} км.")
        else:
            print("Не хватает топлива.")

    def competition(self):
        # Вероятность победы 50%
        if random.random() > 0.5:
            return "Выиграл"
        else:
            return "Проиграл"

car1 = Car(color='черный', fuel=8, fuel_count_100=8)
car2 = SportCar(color='черный', fuel=8, fuel_count_100=8)

print('Первая машина')
for i in range(4):
    car1.drive(30)

print('Вторая машина')
for i in range(4):
    car2.fast_drive(30)

print(car2.competition())