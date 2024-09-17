
# 1

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

# 2

class Programmer:

    SALARIES = {'Junior': 10, 'Middle': 15, 'Senior': 20}

    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.hours_worked = 0
        self.salary_per_hour = self.SALARIES[position]
        self.total_salary = 0
        self.promotions = 0

    def work(self, time):
        self.hours_worked += time
        self.total_salary += time * self.salary_per_hour

    def rise(self):
        if self.position == 'Junior':
            self.position = 'Middle'
            self.salary_per_hour = self.SALARIES['Middle']
        elif self.position == 'Middle':
            self.position = 'Senior'
            self.salary_per_hour = self.SALARIES['Senior']
        elif self.position == 'Senior':
            self.promotions += 1
            self.salary_per_hour = self.SALARIES['Senior'] + self.promotions

    def info(self):
        return f"{self.name} {self.hours_worked}ч. {self.total_salary}тгр."


programmer = Programmer('Васильев Иван', 'Junior')
programmer.work(750)
print(programmer.info())

programmer.rise()
programmer.work(500)
print(programmer.info())

programmer.rise()
programmer.work(250)
print(programmer.info())

programmer.rise()
programmer.work(250)
print(programmer.info())
