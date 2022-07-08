import threading
import datetime
import requests
import json
import uuid
import os

checker_delay = 10
token = ''
devices = {}
scenarios = []

# TRIGGERS ==================================== #

class Interval:
    def __init__(self, parent_scenario, mins):
        self.type = 'interval'
        self.parent_scenario = parent_scenario
        self.mins = mins
        self.activate()
    def engine(self):
        threading.Timer(mins * 60, self.engine)
        for action in parent_scenario.actions:
            action.start()
    def activate(self):
        threading.Timer(mins * 60, self.engine)
    def check(self):
        return False

class Time:
    def __init__(self, parent_scenario, h, m):
        self.type = 'time'
        self.parent_scenario = parent_scenario
        self.hours = h
        self.mins = m
    def check(self):
        if self.hours == datetime.datetime.now().time().split(':')[0] and self.mins == datetime.datetime.now().time().split(':')[1]:
            return True
        return False

# ACTIONS ===================================== #

class On:
    def __init__(self, device_num):
        self.device_num == device_num
    def execute(self):
        set_on_off(self.device_num, 'true')

class Off:
    def __init__(self, device_num):
        self.device_num = device_num
    def execute(self):
        set_on_off(self.device_num, 'false')

class Brightness:
    def __init__(self, device_num, value):
        self.device_num = device_num
        self.value = value
    def execute(self):
        set_brightness(self.device_num, self.value)

class Color_HSV:
    def __init__(self, device_num, h, s, v):
        self.device_num = device_num
        self.h = h
        self.s = s
        self.v = v
    def execute(self):
        set_color_hsv(self.device_num, self.h, self.s, self.v)

class Color_RGB:
    def __init__(self, device_num, r, g, b):
        self.device_num = device_num
        self.r = r
        self.g = g
        self.b = b
    def execute(self):
        set_color_rgb(self.device_num, self.r, self.g, self.b)

class Color_temperature:
    def __init__(self, device_num, value):
        self.device_num = device_num
        self.value = value
    def execute(self):
        set_color_temperature(self.device_num, self.value)

class Color_scene:
    def __init__(self, device_num, scene):
        self.device_num = device_num
        self.value = scene
    def execute(self):
        set_color_scene(self.device_num, self.value)

class Temperature:
    def __init__(self, device_num, value):
        self.device_num = device_num
        self.value = value
    def execute(self):
        set_temperature(self.device_num, self.value)

class Fan_speed:
    def __init__(self, device_num, value):
        self.device_num = device_num
        self.value = value
    def execute(self):
        set_fan_speed(self.device_num, self.value)

class AC_thermostat:
    def __init__(self, device_num, value):
        self.device_num = device_num
        self.value = value
    def execute(self):
        set_ac_thermostat(self.device_num, self.value)

class AC_swing:
    def __init__(self, device_num, value):
        self.device_num = device_num
        self.value = value
    def execute(self):
        set_ac_swing(self.device_num, self.value)

class Enable_ionization:
    def __init__(self, device_num):
        self.device_num = device_num
    def execute(self):
        set_ionization(self.device_num, 'true')

class Disable_ionization:
    def __init__(self, device_num):
        self.device_num = device_num
    def execute(self):
        set_ionization(self.device_num, 'false')
        
class Volume:
    def __init__(self, device_num, value):
        self.device_num = device_num
        self.value = value
    def execute(self):
        set_(self.device_num, self.value)

class Keep_warm_on:
    def __init__(self, device_num):
        self.device_num = device_num
    def execute(self):
        set_keep_warm(self.device_num, 'true')

class Keep_warm_off:
    def __init__(self, device_num):
        self.device_num = device_num
    def execute(self):
        set_keep_warm(self.device_num, 'false')

class Make_coffee:
    def __init__(self, device_num, value):
        self.device_num = device_num
        self.value = value
    def execute(self):
        make_coffee(self.device_num, value)

class Make_tea:
    def __init__(self, device_num, value):
        self.device_num = device_num
        self.value = value
    def execute(self):
        make_tea(self.device_num, self.value)

class Humidity:
    def __init__(self, device_num, value):
        self.device_num = device_num
        self.value = value
    def execute(self):
        set_humidity(self.device_num, self.value)

class Cleanup_mode:
    def __init__(self, device_num, value):
        self.device_num = device_num
        self.value = value
    def execute(self):
        set_cleanup_mode(self.device_num, self.value)

class Cleanup_speed:
    def __init__(self, device_num, value):
        self.device_num = device_num
        self.value = value
    def execute(self):
        set_cleanup_speed(self.device_num, self.value)

class Washing_speed:
    def __init__(self, device_num, value):
        self.device_num = device_num
        self.value = value
    def execute(self):
        set_washing_speed(self.device_num, self.value)

# LIMITATIONS ================================= #

class Time_gap:
    def __init__(self, start_hours, end_hours):
        self.sh = start_hours
        self.eh = end_hours
    def check(self):
        if self.sh < datetime.datetime.now().time().split(':')[0] and self.eh > datetime.datetime.now().time().split(':')[0]:
            return True
        return False

# ============================================= #

def checker_interval():
    threading.Timer(checker_delay, checker_interval).start()
    for scenario in scenarios:
        scenario.check_triggers()

checker_interval()

class Scenario:
    def __init__(self, triggers, actions, limitations):
        self.triggers = triggers
        self.actions = actions
        self.limitations = limitations
    def execute_actions(self):
        for action in self.actions:
            action.execute()
    def check_triggers(self):
        for limitation in self.limitations:
            if not limitation.check():
                return True
        for trigger in self.triggers:
            if trigger.check():
                self.execute_actions()
                break
        return True

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
