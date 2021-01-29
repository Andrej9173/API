import winsound
import json
import pprint
import urllib.request
import time


apikey = '...'
method_get_balance = 'getBalance'  # Узнать баланс
method_getState = 'getState'  # Получить статус
method_getNum = 'getNum'  # Получить номер
method_setRate = 'setRate'  # Ставка

country = 'all'
service = 'service=telegram'
stavka = 0
stavka_parametr = f'rate={stavka}'
# Обнуляем ставку до 0 рублей
url = f'http://api.sms-reg.com/{method_setRate}.php?{stavka_parametr}&apikey={apikey}'
print("Обнуляем ставку")
data_rate = json.loads(urllib.request.urlopen(url).read())  # Считали в json с сайта json
print('Текущая ставка', data_rate['rate'])

while True:
    # Запрос на получение нового номера
    url = f'http://api.sms-reg.com/{method_getNum}.php?{service}&apikey={apikey}'
    print('Запросили новый номер')
    data_json = urllib.request.urlopen(url).read()  # Считали в json с сайта json
    data_correct = json.loads(data_json)  # Преобразовали в питоновский словарь
    tzid = f'tzid={data_correct["tzid"]}'

    # Ожидание получения номера
    # Ждем по 5 секунд 25 раз, итого 120 секунд
    wait = 0
    start = time.time()
    while wait < 24:
        time.sleep(5)
        print('', end='\r') # Эта штука нам нужна, чтобы таймер не писал кучу текста в консоль, а просто обнулялся каждый раз
        url = f'http://api.sms-reg.com/{method_getState}.php?{tzid}&apikey={apikey}'
        data_getState = urllib.request.urlopen(url).read()  # Считали в json с сайта json
        data_getState = json.loads(data_getState)  # Преобразовали в питоновский словарь
        response = data_getState['response']
        if response == 'WARNING_NO_NUMS' or response == 'TZ_INPOOL':
            wait += 1
            # print(wait)
            end = time.time()
            # print('Прошоло', int(end - start), 'секунд')
            print('Прошоло', int(end - start), 'секунд', sep=' ', end='', flush=True)
        else:
            duration = 3000
            freq = 700
            winsound.Beep(freq, duration)
            print('Ура, номер получен')
            break
    # Недождались ответа, повышаем ставку на 1р.
    # И запускаем по новой
    stavka += 1
    stavka_parametr = f'rate={stavka}'
    url = f'http://api.sms-reg.com/{method_setRate}.php?{stavka_parametr}&apikey={apikey}'
    data_rate = urllib.request.urlopen(url).read()  # Считали в json с сайта json
    data_rate = json.loads(data_rate)  # Преобразовали в питоновский словарь
    print()
    print()
    print('Недождались ответа')
    print('Повышаем ставку')
    print('Новая ставка', data_rate['rate'])
