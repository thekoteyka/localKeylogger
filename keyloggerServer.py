import os
from socket import *

from colorama import init, Fore
init(autoreset=False)

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 10000  # Port to listen on (non-privileged ports are > 1023)

s = socket(AF_INET, SOCK_STREAM)  # создаем аналогичный сокет, как у сервера


succesfulConnected = False
count = 1
print(f'{Fore.GREEN}Запуск')
while not succesfulConnected:
    try:
        s.connect(('localhost', PORT))  # коннектимся с сервером
    except ConnectionRefusedError:
        print(f'{Fore.RED}Клиент не запущен, попытка {Fore.CYAN}{count}')
    else:
        succesfulConnected = True
        print(f'{Fore.GREEN}Подключение успешно!')
    count += 1


while True:
    tm = s.recv(1024)  # Принимаем не более 1024 байта данных
    text = tm.decode("utf-8")
    if text != '':
        print(f'{Fore.GREEN}{text}', end='')  # получаем данные, декодировав байты
# s.close()  # закрываем соединение
