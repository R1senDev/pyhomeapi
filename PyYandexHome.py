import threading
import datetime
import requests
import json
import uuid
import os

token = ''
devices = {}
scenarios = []

class Interval:
    def __init__(self, mins):
        if mins == 

def checker_interval():
    threading.Timer(1, checker_interval).start()
    for scenario in scenarios:
        if
        
checker_interval()

class Scenario:
    def __init__(self, triggers, actions, limitations):
        self.triggers = triggers
        self.actions = actions
        self.limitations = limitations

def get_devices_list():
    return requests.get('https://api.iot.yandex.net/v1.0/user/info', headers={'Authorization': f'Bearer {token}'}).json()['devices']

def get_device_state(device_num):
    response = requests.get(f'https://api.iot.yandex.net/v1.0/devices/{devices[device_num]["id"]}', headers={'Authorization': f'Bearer {token}'})
    return response.json()

def set_on_off(device_num, state):
    response = requests.post('https://api.iot.yandex.net/v1.0/devices/actions', headers={'Authorization': f'Bearer {token}', 'X-Request-ID': str(uuid.uuid4()), 'Content-Type': 'application/json'}, data='''{
        "devices": [{
            "id": "''' + devices[device_num]['id'] + '''",
            "custom_data": {
                "api_location": "rus"
            },
            "actions": [{
                "type": "devices.capabilities.on_off",
                "state": {
                    "instance": "on",
                    "value": ''' + state + '''
                }
            }]
        }]
    }''')
    try:
        return response.json()
    except:
        return 'ERROR'

def set_brightness(device_num, value):
    if devices[device_num]['type'] == 'devices.types.light' or devices[device_num]['type'] == 'devices.types.cooking.kettle':
        response = requests.post('https://api.iot.yandex.net/v1.0/devices/actions', headers={'Authorization': f'Bearer {token}', 'X-Request-ID': str(uuid.uuid4()), 'Content-Type': 'application/json'}, data='''{
            "devices": [{
                "id": "''' + devices[device_num]['id'] + '''",
                "custom_data": {
                    "api_location": "rus"
                },
                "actions": [{
                    "type": "devices.capabilities.range",
                    "state": {
                        "instance": "brightness",
                        "value": ''' + str(value) + '''
                    }
                }]
            }]
        }''')
        return response.json()
    else:
        print(f'К сожалению, {devices[device_num]["name"]} не умеет изменять яркость')
        return -1

def set_color_hsv(device_num, hue, saturation, value):
    if devices[device_num]['type'] == 'devices.types.light' or devices[device_num]['type'] == 'devices.types.cooking.kettle':
        response = requests.post('https://api.iot.yandex.net/v1.0/devices/action', headers={'Authorization': f'Bearer {token}', 'X-Request-ID': str(uuid.uuid4()), 'Content-Type': 'application/json'}, data='''{
            "devices": [{
                "id": "''' + devices[device_num]['id'] + '''",
                "custom_data": {
                    "api_location": "rus"
                },
                "actions": [{
                    "type": "devices.capabilities.color_setting",
                    "state": {
                        "instance": "hsv",
                        "value": {
                            "h": ''' + str(hue) + ''',
                            "s": ''' + str(saturation) + ''',
                            "v" : ''' + str(value) + '''
                        }
                    }
                }]
            }]
        }''')
        print(response)
        if str(response) == '<Response [404]>':
            return 404
        return 0
    else:
        print(f'К сожалению, {devices[device_num]["name"]} не умеет изменять цвет')
        return -1

def set_color_rgb(device_num, red, green, blue):
    if devices[device_num]['type'] == 'devices.types.light' or devices[device_num]['type'] == 'devices.types.cooking.kettle':
        response = requests.post('https://api.iot.yandex.net/v1.0/devices/action', headers={'Authorization': f'Bearer {token}', 'X-Request-ID': str(uuid.uuid4()), 'Content-Type': 'application/json'}, data='''{
            "devices": [{
                "id": "''' + devices[device_num]['id'] + '''",
                "custom_data": {
                    "api_location": "rus"
                },
                "actions": [{
                    "type": "devices.capabilities.color_setting",
                    "state": {
                        "instance": "rgb",
                        "value": ''' + str(red) + str(green) + str(blue) + '''
                    }
                }]
            }]
        }''')
        print(response)
        return 0
        if str(response) == '<Response [404]>':
            return 404
    else:
        print(f'К сожалению, {devices[device_num]["name"]} не умеет изменять цвет')

def set_color_temperature(device_num, temperature_k):
    if devices[device_num]['type'] == 'devices.types.light' or devices[device_num]['type'] == 'devices.types.cooking.kettle':
        response = requests.post('https://api.iot.yandex.net/v1.0/user/devices/action', headers={'Authorization': f'Bearer {token}', 'X-Request-ID': str(uuid.uuid4()), 'Content-Type': 'application/json'}, data='''{
            "devices": [{
                "id": "''' + devices[device_num]['id'] + '''",
                "custom_data": {
                    "api_location": "rus"
                },
                "actions": [{
                    "type": "devices.capabilities.color_setting",
                    "state": {
                        "instance": "temperature",
                        "value": "''' + str(temperature) + '''"
                    }
                }]
            }]
        }''')
        if str(response) == '<Response [404]>':
            return '404'
        return response.json()
    else:
        print(f'К сожалению, {devices[device_num]["name"]} не умеет изменять цветовую температуру')
        return -1

def set_color_scene(device_num, scene):
    if devices[device_num]['type'] == 'devices.types.light' or devices[device_num]['type'] == 'devices.types.cooking.kettle':
        response = requests.post('https://api.iot.yandex.net/v1.0/user/devices/action', headers={'Authorization': f'Bearer {token}', 'X-Request-ID': str(uuid.uuid4()), 'Content-Type': 'application/json'}, data='''{
            "devices": [{
                "id": "''' + devices[device_num]['id'] + '''",
                "custom_data": {
                    "api_location": "rus"
                },
                "actions": [{
                    "type": "devices.capabilities.color_setting",
                    "state": {
                        "instance": "scene",
                        "value": "''' + scene + '''"
                    }
                }]
            }]
        }''')
        if str(response) == '<Response [404]>':
            return '404'
        return response.json()
    else:
        print(f'К сожалению, {devices[device_num]["name"]} не умеет изменять цветовую температуру')
        return -1

def set_temperature(device_num, temperature):
    if devices[device_num]['type'] == 'devices.types.thermostat' or devices[device_num]['type'] == 'devices.types.thermostat.ac' or devices[device_num]['type'] == 'devices.types.cooking.kettle':
        response = requests.post('https://api.iot.yandex.net/v1.0/user/devices/action', headers={'Authorization': f'Bearer {token}', 'X-Request-ID': str(uuid.uuid4()), 'Content-Type': 'application/json'}, data='''{
            "devices": [{
                "id": "''' + devices[device_num]['id'] + '''",
                "custom_data": {
                    "api_location": "rus"
                },
                "actions": [{
                    "type": "devices.capabilities.range",
                    "state": {
                        "instance": "temperature",
                        "value": "''' + str(temperature) + '''"
                    }
                }]
            }]
        }''')
        if str(response) == '<Response [404]>':
            return '404'
        return response.json()
    else:
        print(f'К сожалению, {devices[device_num]["name"]} не умеет изменять температуру')
        return -1

# auto | quiet | low | medium | high | turbo #
def set_fan_speed(device_num, mode):
    if devices[device_num]['type'] == 'devices.types.thermostat.ac' or devices[device_num]['type'] == 'devices.types.humidifier' or devices[device_num]['type'] == 'devices.types.purifier':
        response = requests.post('https://api.iot.yandex.net/v1.0/user/devices/action', headers={'Authorization': f'Bearer {token}', 'X-Request-ID': str(uuid.uuid4()), 'Content-Type': 'application/json'}, data='''{
            "devices": [{
                "id": "''' + devices[device_num]['id'] + '''",
                "custom_data": {
                    "api_location": "rus"
                },
                "actions": [{
                    "type": "devices.capabilities.mode",
                    "state": {
                        "instance": "fan_speed",
                        "value": "''' + mode + '''"
                    }
                }]
            }]
        }''')
        if str(response) == '<Response [404]>':
            return '404'
        return response.json()
    else:
        print(f'К сожалению, {devices[device_num]["name"]} не может изменить скорость вентилятора')
        return -1

def set_ac_fan_speed(device_num, mode):
    return set_fan_speed(device_num, mode)

# auto | eco | cool | dry | heat | fan_only #
def set_ac_thermostat(device_num, mode):
    if devices[device_num]['type'] == 'devices.types.thermostat.ac':
        response = requests.post('https://api.iot.yandex.net/v1.0/user/devices/action', headers={'Authorization': f'Bearer {token}', 'X-Request-ID': str(uuid.uuid4()), 'Content-Type': 'application/json'}, data='''{
            "devices": [{
                "id": "''' + devices[device_num]['id'] + '''",
                "custom_data": {
                    "api_location": "rus"
                },
                "actions": [{
                    "type": "devices.capabilities.mode",
                    "state": {
                        "instance": "thermostat",
                        "value": "''' + mode + '''"
                    }
                }]
            }]
        }''')
        if str(response) == '<Response [404]>':
            return '404'
        return response.json()
    else:
        print(f'К сожалению, {devices[device_num]["name"]} не может изменить температуру')

# auto | horisontal | vertical | stationary #
def set_ac_swing(device_num, mode):
    if devices[device_num]['type'] == 'devices.types.thermostat.ac':
        response = requests.post('https://api.iot.yandex.net/v1.0/user/devices/action', headers={'Authorization': f'Bearer {token}', 'X-Request-ID': str(uuid.uuid4()), 'Content-Type': 'application/json'}, data='''{
            "devices": [{
                "id": "''' + devices[device_num]['id'] + '''",
                "custom_data": {
                    "api_location": "rus"
                },
                "actions": [{
                    "type": "devices.capabilities.mode",
                    "state": {
                        "instance": "thermostat",
                        "value": "''' + mode + '''"
                    }
                }]
            }]
        }''')
        if str(response) == '<Response [404]>':
            return '404'
        return response.json()
    else:
        print(f'К сожалению, {devices[device_num]["name"]} не может изменить угол воздушного потока')
        return -1

def set_ionization(device_num, value):
    if devices[device_num]['type'] == 'devices.types.humidifier' or devices[device_num]['type'] == 'devices.types.purifier':
        response = requests.post('https://api.iot.yandex.net/v1.0/user/devices/action', headers={'Authorization': f'Bearer {token}', 'X-Request-ID': str(uuid.uuid4()), 'Content-Type': 'application/json'}, data='''{
            "devices": [{
                "id": "''' + devices[device_num]['id'] + '''",
                "custom_data": {
                    "api_location": "rus"
                },
                "actions": [{
                    "type": "devices.capabilities.toggle",
                    "state": {
                        "instance": "ionization",
                        "value": "''' + str(value).lower() + '''"
                    }
                }]
            }]
        }''')
        if str(response) == '<Response [404]>':
            return '404'
        return response.json()
    else:
        print(f'К сожалению, {devices[device_num]["name"]} не может ионизировать воздух в помещении')
        return -1

def set_volume(device_num, volume):
    response = requests.post('https://api.iot.yandex.net/v1.0/user/devices/action', headers={'Authorization': f'Bearer {token}', 'X-Request-ID': str(uuid.uuid4()), 'Content-Type': 'application/json'}, data='''{
        "devices": [{
            "id": "''' + devices[device_num]['id'] + '''",
            "custom_data": {
                "api_location": "rus"
            },
            "actions": [{
                "type": "devices.capabilities.range",
                "state": {
                    "instance": "volume",
                    "value": "''' + str(volume) + '''"
                }
            }]
        }]
    }''')
    if str(response) == '<Response [404]>':
        return '404'
    return response.json()

def set_keep_warm(device_num, value):
    if devices[device_num]['type'] == 'devices.types.cooking.kettle' or devices[device_num]['type'] == 'devices.types.cooking.multicooker':
        response = requests.post('https://api.iot.yandex.net/v1.0/user/devices/action', headers={'Authorization': f'Bearer {token}', 'X-Request-ID': str(uuid.uuid4()), 'Content-Type': 'application/json'}, data='''{
            "devices": [{
                "id": "''' + devices[device_num]['id'] + '''",
                "custom_data": {
                    "api_location": "rus"
                },
                "actions": [{
                    "type": "devices.capabilities.toggle",
                    "state": {
                        "instance": "keep_warm",
                        "value": "''' + str(value).lower() + '''"
                    }
                }]
            }]
        }''')
        if str(response) == '<Response [404]>':
            return '404'
        return response.json()
    else:
        print(f'К сожалению, {devices[device_num]["name"]} не может сохранять вашу еду или напиток в тёплом состоянии')
        return -1

# americano | cappuccino | latte | espresso | double_espresso #
def make_coffee(device_num, mode):
    if devices[device_num]['type'] == 'devices.types.cooking.coffee_maker':
        response = requests.post('https://api.iot.yandex.net/v1.0/user/devices/action', headers={'Authorization': f'Bearer {token}', 'X-Request-ID': str(uuid.uuid4()), 'Content-Type': 'application/json'}, data='''{
            "devices": [{
                "id": "''' + devices[device_num]['id'] + '''",
                "custom_data": {
                    "api_location": "rus"
                },
                "actions": [{
                    "type": "devices.capabilities.mode",
                    "state": {
                        "instance": "coffee_mode",
                        "value": "''' + mode + '''"
                    }
                }]
            }]
        }''')
        if str(response) == '<Response [404]>':
            return '404'
        return response.json()
    else:
        if mode == 'americano':
            print(f'К сожалению, {devices[device_num]["name"]} не может приготовить вам Американо')
        elif mode == 'capuccino':
            print(f'К сожалению, {devices[device_num]["name"]} не может приготовить вам Капучино')
        elif mode == 'latte':
            print(f'К сожалению, {devices[device_num]["name"]} не может приготовить вам Латте')
        elif mode == 'espresso':
            print(f'К сожалению, {devices[device_num]["name"]} не может приготовить вам Эспрессо')
        elif mode == 'double_espresso':
            print(f'К сожалению, {devices[device_num]["name"]} не может приготовить вам Двойной эспрессо')
        return -1

# black_tea | flower_tea | green_tea | herbal_tea | oolong_tea | puerh_tea | red_tea | white_tea #
def make_tea(device_num, mode):
    if devices[device_num]['type'] == 'devices.types.cooking.kettle':
        response = requests.post('https://api.iot.yandex.net/v1.0/user/devices/action', headers={'Authorization': f'Bearer {token}', 'X-Request-ID': str(uuid.uuid4()), 'Content-Type': 'application/json'}, data='''{
            "devices": [{
                "id": "''' + devices[device_num]['id'] + '''",
                "custom_data": {
                    "api_location": "rus"
                },
                "actions": [{
                    "type": "devices.capabilities.mode",
                    "state": {
                        "instance": "tea_mode",
                        "value": "''' + mode + '''"
                    }
                }]
            }]
        }''')
        if str(response) == '<Response [404]>':
            return '404'
        return response.json()
    else:
        if mode == 'black_tea':
            print(f'К сожалению, {devices[device_num]["name"]} не может приготовить вам Чёрный чай')
        elif mode == 'flower_tea':
            print(f'К сожалению, {devices[device_num]["name"]} не может приготовить вам Цветочный чай')
        elif mode == 'green_tea':
            print(f'К сожалению, {devices[device_num]["name"]} не может приготовить вам Зелёный чай')
        elif mode == 'herbal_tea':
            print(f'К сожалению, {devices[device_num]["name"]} не может приготовить вам Травяной чай')
        elif mode == 'oolong_tea':
            print(f'К сожалению, {devices[device_num]["name"]} не может приготовить вам Улун')
        elif mode == 'puerh_tea':
            print(f'К сожалению, {devices[device_num]["name"]} не может приготовить вам Пуэр')
        elif mode == 'red_tea':
            print(f'К сожалению, {devices[device_num]["name"]} не может приготовить вам Красный чай')
        elif mode == 'white_tea':
            print(f'К сожалению, {devices[device_num]["name"]} не может приготовить вам Белый чай')
        return -1

# slow | medium | fast #
def opening_speed(device_num, speed):
    if devices[device_num]['type'] == 'devices.types.openable' or devices[device_num]['type'] == 'devices.types.openable.curtain':
        response = requests.post('https://api.iot.yandex.net/v1.0/user/devices/action', headers={'Authorization': f'Bearer {token}', 'X-Request-ID': str(uuid.uuid4()), 'Content-Type': 'application/json'}, data='''{
            "devices": [{
                "id": "''' + devices[device_num]['id'] + '''",
                "custom_data": {
                    "api_location": "rus"
                },
                "actions": [{
                    "type": "devices.capabilities.mode",
                    "state": {
                        "instance": "work_speed",
                        "value": "''' + speed + '''"
                    }
                }]
            }]
        }''')
        if str(response) == '<Response [404]>':
            return '404'
        return response.json()
    else:
        print(f'К сожалению, {devices[device_num]["name"]} не может изменить скорость открытия')
        return -1

def set_humidity(device_num, level):
    if devices[device_num]['type'] == 'devices.types.humidifier':
        response = requests.post('https://api.iot.yandex.net/v1.0/user/devices/action', headers={'Authorization': f'Bearer {token}', 'X-Request-ID': str(uuid.uuid4()), 'Content-Type': 'application/json'}, data='''{
            "devices": [{
                "id": "''' + devices[device_num]['id'] + '''",
                "custom_data": {
                    "api_location": "rus"
                },
                "actions": [{
                    "type": "devices.capabilities.range",
                    "state": {
                        "instance": "humidity",
                        "value": "''' + level + '''"
                    }
                }]
            }]
        }''')
        if str(response) == '<Response [404]>':
            return '404'
        return response.json()
    else:
        print(f'К сожалению, {devices[device_num]["name"]} не может контролировать влажность в помещении')

# auto | eco | quiet | normal | express #
def set_cleanup_mode(device_num, mode):
    if devices[device_num]['type'] == 'devices.types.vacuum_cleaner':
        response = requests.post('https://api.iot.yandex.net/v1.0/user/devices/action', headers={'Authorization': f'Bearer {token}', 'X-Request-ID': str(uuid.uuid4()), 'Content-Type': 'application/json'}, data='''{
            "devices": [{
                "id": "''' + devices[device_num]['id'] + '''",
                "custom_data": {
                    "api_location": "rus"
                },
                "actions": [{
                    "type": "devices.capabilities.mode",
                    "state": {
                        "instance": "cleanup_mode",
                        "value": "''' + mode + '''"
                    }
                }]
            }]
        }''')
        if str(response) == '<Response [404]>':
            return '404'
        return response.json()
    else:
        print(f'К сожалению, {devices[device_num]["name"]} не может изменять режим уборки')
    
    # auto | slow | mmedium | fast | turbo #
def set_cleanup_speed(device_num, speed):
    if devices[device_num]['type'] == 'devices.types.vacuum_cleaner':
        response = requests.post('https://api.iot.yandex.net/v1.0/user/devices/action', headers={'Authorization': f'Bearer {token}', 'X-Request-ID': str(uuid.uuid4()), 'Content-Type': 'application/json'}, data='''{
            "devices": [{
                "id": "''' + devices[device_num]['id'] + '''",
                "custom_data": {
                    "api_location": "rus"
                },
                "actions": [{
                    "type": "devices.capabilities.mode",
                    "state": {
                        "instance": "cleanup_mode",
                        "value": "''' + mode + '''"
                    }
                }]
            }]
        }''')
        if str(response) == '<Response [404]>':
            return '404'
        return response.json()
    else:
        print(f'К сожалению, {devices[device_num]["name"]} не может изменять скорость уборки')

# auto | eco | quiet | glass | express | pre_rinse | intensive #
def set_washing_speed(device_num, mode):
    if devices[device_num]['type'] == 'devices.types.dishwasher':
        response = requests.post('https://api.iot.yandex.net/v1.0/user/devices/action', headers={'Authorization': f'Bearer {token}', 'X-Request-ID': str(uuid.uuid4()), 'Content-Type': 'application/json'}, data='''{
            "devices": [{
                "id": "''' + devices[device_num]['id'] + '''",
                "custom_data": {
                    "api_location": "rus"
                },
                "actions": [{
                    "type": "devices.capabilities.mode",
                    "state": {
                        "instance": " dishwashing",
                        "value": "''' + mode + '''"
                    }
                }]
            }]
        }''')
        if str(response) == '<Response [404]>':
            return '404'
        return response.json()
    else:
        print(f'К сожалению, {devices[device_num]["name"]} не может изменять скорость мытья посуды')

if os.path.exists('token.txt'):
    file = open('token.txt', 'r')
    token = file.read()
    token = token[:len(token) - 1]
    if token == '':
        token = input('Введите токен приложения: ')
        file.close()
        with open('file.txt', 'w') as file:
            file.write(token)
else:
    token = input('Введите токен приложения: ')
    with open('token.txt', 'x') as file:
        file.write(token)

i = 1
try:
    for device in get_devices_list():
        devices[i] = {}
        devices[i]['name'] = device['name']
        devices[i]['id'] = device['id']
        devices[i]['type'] = device['type']
        i += 1
except:
    print('Ошибка! Проверьте правильность токена, изменив файл token.txt')
