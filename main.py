import requests
import re
from collections import Counter
req = requests.Session()
import time

lst = []

comparer = 0
hourly = 0
daily = 0
sales_daily = 0
sales_hourly = 0
full_id = 0

webhook = 'put your webhook here'
groupid = 'put groupid here'
cookie = 'put cookie here'

def sales():
    req.cookies['.ROBLOSECURITY'] = cookie
    r = req.get(f'https://economy.roblox.com/v2/groups/{groupid}/transactions?cursor=&limit=100&sortOrder=Asc&transactionType=Sale').json()['data']
    c = 0
    for i in range(50):
        t = r[c]
        saleid = t['id']
        userid = t['agent']['id']
        username = t['agent']['name']
        clothingid = t['details']['id']
        clothing_name = t['details']['name']
        price = t['currency']['amount']
        lst.append(f'{username}:{userid}:{clothing_name}:{price}:{saleid}:{clothingid}')
        c += 1

def number(lst):
    n = lst.split(':')[4]
    return int(n)

def check():
    global sales_hourly
    global sales_daily
    global hourly
    global daily
    global comparer

    lst.sort(key=number)

    counts = Counter(lst)
    for line in counts:
        if counts[line] == 1:
            time.sleep(0.1)
            sales_hourly += 1
            sales_daily += 1
            user, userid, clothing_name, price, saleid, clothingid = line.split(':',6)
            if int(saleid) > int(comparer):
                data = {
                      'embeds':[{
                          'author': {
                              'name': f'Asset Sold'
                              },
                          'color': int('0099E1',16),
                          'fields': [
                              {'name': '\u200b', 'value': f'**User**: {user}\n**UserID**: {userid}\n**Price**: {price}', 'inline':False},
                              {'name': '\u200b', 'value': f'**Daily Sales**: {sales_daily}\n**Hourly Sales**: {sales_hourly}', 'inline':False},
                              {'name': '\u200b', 'value': f'**Asset**: {clothing_name}\n**Asset ID**: {clothingid}', 'inline':False},
                          ],
                          'thumbnail': {
                              'url': f'https://www.roblox.com/headshot-thumbnail/image?userId={userid}&width=420&height=420&format=png',
                              }
                    }]
                  }
                r = requests.post(webhook,json=data).text
            else: pass
            comparer = int(saleid)

sales()
time.sleep(60)


while True:
    sales()
    check()
    print('checked')
    time.sleep(60)
    if daily % 60 == 0:
        daily -= daily
    else: pass

    if hourly % 1440 == 0:
        hourly -= hourly
    else: pass
    # i dont know if the reset sales count hourly and daily even works properly
