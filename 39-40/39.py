
# 1

def rub_to_dollars(rubs, rate):
    return rubs/rate

rubs = int(input('введите количество рублей: '))
rate = int(input('введите курс доллара(руб/доллар): '))

print(f'{rub_to_dollars(rubs, rate)} долларов')

# 2

def is_adult(age):
    return True if age >= 18 else False

age = int(input('enter your age: '))

print(is_adult(age))