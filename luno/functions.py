import configparser
import requests
import json

class lunoFunctions():

    def __init__(self):

        config = configparser.ConfigParser()
        config.read('./config.ini')  
        self.CONFIG = config
        self.BASE_URL = config['DEFAULT']['base_url']
        self.AUTH = (config['DEFAULT']['api_key'], config['DEFAULT']['api_token'])
        self.LOOP_INTERVAL = int(config['DEFAULT']['loop_interval'])
        self.AVERAGE_LIST_LENGTH = int(config['DEFAULT']['average_list_length'])
        self.AMOUNT_TO_TRADE = config['DEFAULT']['amount_to_trade']
        self.MODE = int(config['DEFAULT']['mode'])
        self.ORDER = config['DEFAULT']['order_id']
        self.PAIR = config['DEFAULT']['pair']
        self.START_DELAY = int(config['DEFAULT']['start_delay'])

    def update_config(self):
        with open('./config.ini', 'w') as configfile: 
            self.CONFIG.write(configfile)
        return

    def start_delay(self):
        return self.START_DELAY

    def price(self):
        PARAMS = {
            'pair': self.PAIR
            }
        try:
            res = requests.get(self.BASE_URL + 'ticker', params=PARAMS, auth=self.AUTH)
            res = json.loads(res.content.decode('utf-8'))
            return float(res['last_trade'])
        except Exception:
            return 0

    def loop_frequency(self):
        return self.LOOP_INTERVAL

    def init_average(self, price):
        averages = []
        for i in range(self.AVERAGE_LIST_LENGTH):
            averages.append(price)

        return averages

    def update_averages(self, averages, price):
        new_moving_averages = []
        for i in range(self.AVERAGE_LIST_LENGTH):
            if i == 0:
                new_moving_averages.append(price)
            else:
                new_moving_averages.append(averages[i - 1]) 
        return new_moving_averages

    def get_average(self, averages):
        average = sum(averages) / self.AVERAGE_LIST_LENGTH
        return round(average, 2)

    def get_mode(self):
        return self.MODE

    def get_order(self):
        return self.ORDER

    def delete_order(self, order_id):
        PARAMS = {
            'order_id': order_id
        }
        res = requests.post(self.BASE_URL + 'stoporder', params=PARAMS, auth=self.AUTH)
        res = json.loads(res.content.decode('utf-8'))
        return

    def place_buy_order(self, buy_price):
        PARAMS = {
            'pair': self.PAIR,
            'type': "BID",
            "post_only": True,
            "volume": self.AMOUNT_TO_TRADE,
            "price": buy_price
        }
        try:
            res = requests.post(self.BASE_URL + 'postorder', params=PARAMS, auth=self.AUTH)
            res = json.loads(res.content.decode('utf-8'))
            return res['order_id']
        except Exception:
            return "N/A"

    def buyer(self, price, average, minimum_price, maximum_price):
        if price == maximum_price and price == minimum_price:
            return "N/A"
        elif minimum_price >= average:
            return "N/A"
        else:
            order = self.place_buy_order(minimum_price)
            return order

    def store_order_id(self, order):
        self.CONFIG['DEFAULT']['order_id'] = order
        self.ORDER = order
        self.update_config()
        return      

    def update_mode(self, mode):
        self.CONFIG['DEFAULT']['mode'] = str(mode)
        self.MODE = mode
        self.update_config()
        return mode

    def check_order(self, order_id, mode, minimum_price):
        PARAMS = {
            'id': order_id
        }
        res = requests.get(self.BASE_URL + 'orders/' + order_id, params=PARAMS, auth=self.AUTH)
        res = json.loads(res.content.decode('utf-8'))
        if res['state'] == "COMPLETE":
            if res['type'] == "BID":
                mode = 2
            else:
                mode = 1
        if mode == 3:
            if res['type'] == "BID" and float(res['limit_price']) != minimum_price:
                self.delete_order(order_id)
                mode = 1
        return mode

    def place_sell_order(self, sell_price):
        PARAMS = {
            'pair': self.PAIR,
            'type': "ASK",
            "post_only": True,
            "volume": self.AMOUNT_TO_TRADE,
            "price": sell_price
        }
        try:
            res = requests.post(self.BASE_URL + 'postorder', params=PARAMS, auth=self.AUTH)
            res = json.loads(res.content.decode('utf-8'))
            return res['order_id']
        except Exception:
            return "N/A"

    def seller(self, price, average, minimum_price, maximum_price):
        order = self.place_sell_order(round(average))
        return order
