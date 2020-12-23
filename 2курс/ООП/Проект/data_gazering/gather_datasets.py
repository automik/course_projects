import requests
import pandas as pd
import datetime
import json
import time

# import random

df = pd.read_csv('data/SECID.csv')
print(df)
total_data = {'features': [], 'predict': []}
streak = 0
max_streak = 0
previous_code = df.at[0, 'SECID']
data_length = 300
data_test_length = 25

start_counting_time = datetime.datetime.now()

for index, code_i in df.iterrows():

    code = code_i['SECID']
    streak = 0

    date = datetime.date(day=1, month=1, year=2005)

    req = requests.get(f'https://iss.moex.com/iss/history/engines/stock/markets/shares/boards/TQBR/securities/'
                       f'{code}.jsonp?from={date.strftime("%Y-%m-%d")}&iss.meta=off&iss.json=extended&callback=angular.callbacks._s&_=1608126939154')

    text = req.text
    text = text[22:-2]

    my_data = json.loads(text)
    start_price = my_data[1]['history'][0]['LEGALCLOSEPRICE']
    current_date = datetime.datetime.strptime(my_data[1]['history'][0]['TRADEDATE'], '%Y-%m-%d').date()

    while (current_date + datetime.timedelta(days=600)) < datetime.date.today():
        data = [[], []]

        while (len(data[0]) + len(data[1])) < data_length:
            time.sleep(0.5)
            req = requests.get(f'https://iss.moex.com/iss/history/engines/stock/markets/shares/boards/TQBR/securities/'
                               f'{code}.jsonp?from={current_date.strftime("%Y-%m-%d")}&iss.meta=off&iss.json=extended&callback=angular.callbacks._s&_=1608126939154')

            text = req.text
            text = text[22:-2]
            my_data = json.loads(text)

            if (current_date + datetime.timedelta(days=150)) > datetime.datetime.now().date():
                break

            if len(my_data[1]['history']) == 0:
                current_date += datetime.timedelta(days=50)
                continue
            previous_day = my_data[1]['history'][0]
            counter = 1
            while (previous_day['LEGALCLOSEPRICE'] is None) and (counter < len(my_data[1]['history'])):
                previous_day = my_data[1]['history'][counter]
                counter += 1

            if counter == len(my_data[1]['history']):
                current_date += datetime.timedelta(days=100)
                continue

            for i in range(counter, len(my_data[1]['history'])):
                if (len(data[0]) + len(data[1])) == data_length:
                    break
                day = my_data[1]['history'][i]
                current_date = datetime.datetime.strptime(day['TRADEDATE'], '%Y-%m-%d').date()
                if day['LEGALCLOSEPRICE'] is None:
                    continue

                if len(data[0]) >= (data_length - data_test_length):
                    data[1].append(day['LEGALCLOSEPRICE']-previous_day['LEGALCLOSEPRICE'])
                else:
                    data[0].append(day['LEGALCLOSEPRICE']-previous_day['LEGALCLOSEPRICE'])
                previous_day = day
        if code == previous_code:
            streak += 1
        else:
            streak = 1
        if streak > max_streak:
            max_streak = streak
        if (data[0].count(0) + data[1].count(0)) > (data_length//2):
            continue
        if (len(data[0]) + len(data[1])) == data_length:
            max_dif = max(max(data[0]), max(data[1]))
            min_dif = min(min(data[0]), min(data[1]))
            if (max_dif-min_dif) == 0:
                max_dif += max_dif/10
            for i in range(len(data[0])):
                data[0][i] = (data[0][i] - min_dif)/(max_dif-min_dif)
            for i in range(len(data[1])):
                data[1][i] = (data[1][i] - min_dif)/(max_dif-min_dif)

            total_data['features'].append(data[0])
            total_data['predict'].append(data[1])

            print(f'Total_length: {len(total_data["features"])}, streak: {streak},'
                  f' code: {code}, index: {index}, max_streak: {max_streak}, current_date: {current_date}', data)
        previous_code = code
write_data = pd.DataFrame(total_data)
write_data.to_csv('data/DATASETS.csv', mode='w', index=False)
print(f'finished in {datetime.datetime.now() - start_counting_time}')
