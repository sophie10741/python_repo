class BankAccount:
    def __init__(self, account_holder, initial_balance=0):
        """Инициализация банковского счета."""
        self.account_holder = account_holder
        self.balance = initial_balance

    def deposit(self, amount):
        """Внесение денег на счет."""
        if amount <= 0:
            return "Сумма вклада должна быть положительной."
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        """Снятие денег со счета."""
        if amount <= 0:
            return "Сумма снятия должна быть положительной."
        if amount > self.balance:
            return "Недостаточно средств на счете."
        self.balance -= amount
        return self.balance

    def get_balance(self):
        """Получение текущего баланса."""
        return self.balance


# Тесты
import unittest

class TestBankAccount(unittest.TestCase):
    def setUp(self):
        """Создаем экземпляр BankAccount для тестов"""
        self.account = BankAccount("Тестовый пользователь", 1000)

    def test_initial_balance(self):
        """Тест начального баланса при создании счета"""
        self.assertEqual(self.account.get_balance(), 1000, "Начальный баланс должен быть 1000")

    def test_deposit_positive_amount(self):
        """Тест внесения положительной суммы"""
        self.account.deposit(500)
        self.assertEqual(self.account.get_balance(), 1500, "Баланс должен увеличиться на 500")

    def test_deposit_zero_amount(self):
        """Тест внесения нулевой суммы"""
        result = self.account.deposit(0)
        self.assertEqual(result, "Сумма вклада должна быть положительной.", "Нулевая сумма должна возвращать предупреждение")
        self.assertEqual(self.account.get_balance(), 1000, "Баланс не должен измениться при нулевом депозите")

    def test_deposit_negative_amount(self):
        """Тест внесения отрицательной суммы"""
        result = self.account.deposit(-100)
        self.assertEqual(result, "Сумма вклада должна быть положительной.", "Отрицательная сумма должна возвращать предупреждение")
        self.assertEqual(self.account.get_balance(), 1000, "Баланс не должен измениться при отрицательном депозите")

    def test_withdraw_positive_amount(self):
        """Тест снятия положительной суммы, когда средств достаточно"""
        self.account.withdraw(500)
        self.assertEqual(self.account.get_balance(), 500, "Баланс должен уменьшиться на 500")

    def test_withdraw_amount_greater_than_balance(self):
        """Тест снятия суммы, превышающей баланс"""
        result = self.account.withdraw(1500)
        self.assertEqual(result, "Недостаточно средств на счете.", "Должно вернуться предупреждение о недостатке средств")
        self.assertEqual(self.account.get_balance(), 1000, "Баланс не должен измениться при превышении суммы снятия")

    def test_withdraw_zero_amount(self):
        """Тест снятия нулевой суммы"""
        result = self.account.withdraw(0)
        self.assertEqual(result, "Сумма снятия должна быть положительной.", "Нулевая сумма должна возвращать предупреждение")
        self.assertEqual(self.account.get_balance(), 1000, "Баланс не должен измениться при нулевом снятии")

    def test_withdraw_negative_amount(self):
        """Тест снятия отрицательной суммы"""
        result = self.account.withdraw(-200)
        self.assertEqual(result, "Сумма снятия должна быть положительной.", "Отрицательная сумма должна возвращать предупреждение")
        self.assertEqual(self.account.get_balance(), 1000, "Баланс не должен измениться при отрицательном снятии")

    def test_get_balance(self):
        """Тест получения текущего баланса"""
        self.assertEqual(self.account.get_balance(), 1000, "Метод get_balance должен возвращать текущий баланс")

if __name__ == "__main__":
    unittest.main()
