import requests
import pandas as pd

if __name__ == '__main__':
    req = requests.get(
        'https://iss.moex.com/iss/engines/stock/markets/shares/boardgroups/57/securities.jsonp?iss.meta=off&iss.json=extended&callback=angular.callbacks._k&security_collection=3&sort_column=SHORTNAME&sort_order=asc&lang=ru&_=1608203668291')

    text = req.text
    key = '"SECID": "'
    code_list = []
    while text.count(key) > 0:
        code = text[text.index(key) + 10:text.index(key) + 15]
        if code[-1] == '"':
            code = code[:-1]
        if code not in code_list:
            code_list.append(code)
        text = text.replace(key+code+'"', '0'*15, 2)

    df = pd.DataFrame(code_list, columns=['SECID'])
    df.to_csv('data/SECID.csv', index=False)
