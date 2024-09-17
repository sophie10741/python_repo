
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

my_car = Car("black", 50, 8)
my_car.drive(200)
print(f"Пробег: {my_car.get_mileage()} км")
my_car.drive(400)
my_car.drive(1000)