import requests, json, time, random, datetime
from threading import Thread

with open('config.json') as config:
    config = json.load(config)

with requests.Session() as session:
    session.cookies['.ROBLOSECURITY'] = config['cookie']

class Group():

    def __init__(self):
        pass

    def initialSales(self):
        response = session.get(f'https://economy.roblox.com/v2/groups/{config["group_id"]}/transactions?cursor=&limit=100&sortOrder=Asc&transactionType=Sale').json()['data']
        self.previousSales = [sale['id'] for sale in response]

    def getHourly(self, response):
        hourlySales = hourlyGain = 0
        currentUnix = int(time.time())
        for sale in response:
            date = sale['created'].split('.')[0].replace('T', ' ')
            dt = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            saleUnix = time.mktime(dt.timetuple())
            if currentUnix-3600 <= saleUnix+3600: # i don't know why everytime i convert these sale times to unix they have -3600 less, but anyways i just +3600 to fix that i guess
                hourlySales += 1
                hourlyGain += sale['currency']['amount']
        return hourlySales, hourlyGain

    def constantCheck(self):
        while True:
            try:
                response = session.get(f'https://economy.roblox.com/v2/groups/{config["group_id"]}/transactions?cursor=&limit=100&sortOrder=Asc&transactionType=Sale').json()['data']

                hourlySales, hourlyGain = self.getHourly(response)

                for sale in response:
                    if sale['id'] not in self.previousSales:

                        data = {
                            'embeds':[{
                                'author': {
                                    'name': f'{sale["details"]["name"]}'
                                    },
                                'color': int('0099E1',16),
                                'fields': [
                                    {'name': 'Buyer', 'value': f'{sale["agent"]["name"]}', 'inline':True},
                                    {'name': 'Price', 'value': f'{sale["currency"]["amount"]}', 'inline':True},
                                    {'name': 'Statistics', 'value': f'Past Hour Sales: {hourlySales}\nPast Hour Gain: R$ {hourlyGain}', 'inline':False},
                                ],
                                'thumbnail': {
                                    'url': f'https://www.roblox.com/headshot-thumbnail/image?userId={sale["agent"]["id"]}&width=420&height=420&format=png',
                                    }
                            }]
                        }
                        requests.post(config['webhook'], json=data)

                self.previousSales = [sale['id'] for sale in response]
                time.sleep(60)

            except:
                time.sleep(5)
                pass

a = Group()
a.initialSales()
a.constantCheck()
