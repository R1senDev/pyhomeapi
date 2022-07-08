import os
os.system('clear')
print('Импорт библиотек...')
import requests
import json
import uuid
from colorama import init
init()
from colorama import Fore
os.system('clear')
print('Загрузка...')
import PyYandexHome as pyh

os.system('clear')
print(Fore.GREEN + 'Ваши устройства:' + Fore.WHITE + '\n')
i = 1
for device in pyh.devices:
    print(Fore.GREEN + '[' + str(i) + ']' + Fore.WHITE + ' ' + pyh.devices[i]['name'])
    i += 1
print()

#print(requests.get('https://api.iot.yandex.net/v1.0/user/info', headers={'Authorization': 'Bearer AQAAAAA8Th9IAAgJ5Ddxm6JixkC7q6_XsgyrCG4'}).json())

active_device = int(input('Введите номер устройства, с которым хотите взаимодействовать: '))
if active_device >= 1 and active_device <= len(pyh.devices):
    os.system('clear')
    print(f'Что {Fore.GREEN}{pyh.devices[active_device]["name"]}{Fore.WHITE} должен(на) сделать?\n\n{Fore.GREEN}[01]{Fore.WHITE} Включить\n{Fore.GREEN}[02]{Fore.WHITE} Выключить\n{Fore.GREEN}[03]{Fore.WHITE} Изменить яркость\n{Fore.GREEN}[04]{Fore.WHITE} Изменить цвет (HSV)\n{Fore.GREEN}[05]{Fore.WHITE} Изменить цвет (RGB)\n{Fore.GREEN}[06]{Fore.WHITE} Изменить цветовую температуру\n{Fore.GREEN}[07]{Fore.WHITE} Изменить режим подсветки\n{Fore.GREEN}[08]{Fore.WHITE} Установить температуру\n{Fore.GREEN}[09]{Fore.WHITE} Изменить скорость вентилятора\n{Fore.GREEN}[10]{Fore.WHITE} Изменить температуру кондиционера\n{Fore.GREEN}[11]{Fore.WHITE} Изменить угол воздушного потока\n{Fore.GREEN}[12]{Fore.WHITE} Включить ионизацию воздуха\n{Fore.GREEN}[13]{Fore.WHITE} Выключить ионизацию воздуха\n{Fore.GREEN}[14]{Fore.WHITE} Установить громкость\n{Fore.GREEN}[15]{Fore.WHITE} Включить поддержку тепмературы еды/жидкости\n{Fore.GREEN}[16]{Fore.WHITE} Выключить поддержку температуры еды/жидкости\n{Fore.GREEN}[17]{Fore.WHITE} Приготовить кофе\n{Fore.GREEN}[18]{Fore.WHITE} Приготовить чай\n{Fore.GREEN}[19]{Fore.WHITE} Изменить скорость открытия\n{Fore.GREEN}[20]{Fore.WHITE} Изменить влажность\n{Fore.GREEN}[21]{Fore.WHITE} Установить режим уборки\n{Fore.GREEN}[22]{Fore.WHITE} Изменить скорость уборки\n{Fore.GREEN}[23]{Fore.WHITE} Изменить скорость мытья посуды\n\n')
    action = int(input('Введите номер необходимого действия: '))
    if action == 1:
        pyh.set_on_off(active_device, 'true')
    elif action == 2:
        pyh.on_off(active_device, 'false')
    elif action == 3:
        value = int(input('\nВведите значение яркости (1–100): '))
        pyh.set_brightness(active_device, value)
    elif action == 4:
        h = int(input('\nТон: '))
        s = int(input('Насыщенность: '))
        v = int(input('Значение: '))
        pyh.set_color_hsv(active_device, h, s, v)
    elif action == 5:
        r = int(input(f'\n{Fore.RED}Красный:{Fore.WHITE} '))
        g = int(input(f'{Fore.GREEN}Зелёный:{Fore.WHITE} '))
        b = int(input(f'{Fore.BLUE}Синий:{Fore.WHITE} '))
        pyh.set_color_rgb(active_device, r, g, b)
    elif action == 6:
        value = int(input('\nВведите цветовую температуру (1500-6500): '))
        pyh.set_color_temperature(active_device, value)
    elif action == 7:
        value = input('Введите название режима: ')
        pyh.set_color_scene(active_device, value)
    elif action == 8:
        value = int(input('Введите температуру (°С): '))
        pyh.set_temperature(active_device, value)
    elif action == 9:
        #скорость вентилятора
        value = input('[1] Авто\n[2] Тихий\n[3] Медленно\n[4] Средне\n[5] Быстро\n[6] Турбо\n')
        pyh.set_fan_speed(active_device, value)
    #elif action == 10:
        #тепература конд
    #elif action == 11:
        #угол воздушного потока
    #elif action == 12:
        #ион включить
    #elif action == 13:
        #ион выключить
    #elif action == 14:
        #громкость
    #elif action == 15:
        #поддержка +
    #elif action == 16:
        #поддержка -
    #elif action == 17:
        #кофе
    #elif action == 18:
        #чай
    #elif action == 19:
        #скрорсть откр
    #elif action == 20:
        #влажность
    #elif action == 21:
        #режим уборки
    #elif action == 22:
        #скорость уборки
    #elif action == 23;
        #скорость мытья посуды
