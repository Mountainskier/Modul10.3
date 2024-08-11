import threading
import random
import time


class Bank:
    def __init__(self):
        self.balance = 0
        self.lock = threading.Lock()

    def deposit(self):
        for _ in range(100):
            numbers = random.randint(50, 500)
            with self.lock:
                self.balance += numbers
                print(f'Пополнение: {numbers}. Баланс: {self.balance}')
                if self.balance >= 500 and self.lock.locked():
                    self.lock.release()
            time.sleep(0.001)

    def take(self):
        for _ in range(100):
            numbers = random.randint(50, 500)
            print(f'Запрос на {numbers}')
            with self.lock:
                if numbers <= self.balance:
                    self.balance -= numbers
                    print(f'Снятие: {numbers}. Баланс: {self.balance}')
                else:
                    print('Запрос отклонён, недостаточно средств')
                    self.lock.acquire()
            time.sleep(0.001)


bk = Bank()

th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()

th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')
