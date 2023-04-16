import json
from datetime import datetime, timedelta
from typing import Literal

import ccxt
import redis as redis

from trading_bot.exchange_extra.currency_pair import CurrencyPair
from .balance import Balance
from .time import date_format


class OrderManager:
    def __init__(self, currency_pair: CurrencyPair, api: ccxt.Exchange, redis_client: redis.Redis):
        self.currency_pair = currency_pair
        # self.api: ccxt.binance
        self.api = api
        self.redis_client = redis_client
        self.balance = Balance(self.currency_pair, self.api, self.redis_client)

    async def create_order(self, order_side: Literal['buy', 'sell'], price,
                           order_type: Literal['limit', 'market'] = 'limit'):
        if not price or not order_side:
            return None

        # Check if there is enough TUSD available to buy BTC
        amount = await self.balance.get_available_amount(order_side, price)
        if amount == 0:
            return None

        symbol = self.currency_pair.get_symbol()
        min_trade_amount = self.api.markets[symbol]['limits']['amount']['min']
        if amount < min_trade_amount:
            return None

        order_data = self.api.create_order(symbol, order_type, order_side, amount, price)
        self.redis_client.hset('orders', order_data['id'], json.dumps(order_data))

        print(
            f"{self.get_order_date(order_data)} [{symbol}] {order_side.upper()} {order_data['amount']} {self.currency_pair.get_base()} for {order_data['price']} {self.currency_pair.get_quote()}"
        )

    async def get_order_status(self, order_id):
        if order_id:
            # Get order status from redis
            order_data = self.redis_client.hget('orders', order_id)
            if order_data:
                order_data = self.normalize_order_data(order_data)
                return order_data['status']
            else:
                # Get order status from exchange
                fetched_order = await self.api.fetch_order(order_id, self.currency_pair.get_symbol())
                return fetched_order['status']
        else:
            return None

    async def cancel_order(self, order_data):
        if not order_data:
            return None

        order_data = self.normalize_order_data(order_data)
        order_status = await self.get_order_status(order_data['id'])
        if order_status != 'open':
            return None

        await self.api.cancel_order(order_data['id'], self.currency_pair.get_symbol())
        print(f"#{order_data['id']} order was canceled.")
        # Remove order from redis
        self.redis_client.hdel('orders', order_data['id'])

    async def cancel_order_if_timeout(self, order_data, timeout):
        if not order_data:
            return None

        order_data = self.normalize_order_data(order_data)
        order_status = await self.get_order_status(order_data['id'])
        if order_status != 'open':
            # TODO: implement order history
            remove_order = self.redis_client.hdel('orders', order_data['id'])
            return None

        order_time = datetime.fromtimestamp(self.normalize_order_timestamp(order_data['timestamp']))
        timeout_delta = timedelta(seconds=timeout)
        if datetime.now() - order_time > timeout_delta:
            await self.cancel_order(order_data)
            print(f"#{order_data['orderId']} order was canceled by timeout.")

    def get_open_orders(self):
        return self.redis_client.hgetall('orders')

    @staticmethod
    def normalize_order_data(order_data):
        if not order_data:
            return None
        if isinstance(order_data, bytes):
            order_data = json.loads(order_data.decode())
        return order_data

    @staticmethod
    def normalize_order_timestamp(t: int):
        return t / 1000

    def get_order_date(self, order_data):
        if not order_data:
            return None
        return date_format(self.normalize_order_timestamp(order_data['timestamp']))
