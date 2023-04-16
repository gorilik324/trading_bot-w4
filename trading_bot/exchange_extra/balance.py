import asyncio
import json
from typing import Literal

import ccxt
import redis as redis
from ccxt import decimal_to_precision, TRUNCATE

from trading_bot.exchange_extra.currency_pair import CurrencyPair


class Balance:
    def __init__(self, currency_pair: CurrencyPair, api: ccxt.Exchange, redis_client: redis.Redis):
        self.currency_pair = currency_pair
        self.api = api
        self.redis_client = redis_client

    async def get_currency_balance(self, currency: str) -> float:
        # Get balance from redis
        balance = self.redis_client.hget('balance', 'data')
        if balance:
            data = json.loads(balance)
            return float(data[currency]['free'])

        # Get balance from exchange
        balance = await asyncio.to_thread(self.api.fetch_balance)
        self.redis_client.hset('balance', 'data', json.dumps(balance))
        return float(balance[currency]['free'])

    # Get available amount for the given order type
    async def get_available_amount(
            self, order_side: Literal['buy', 'sell'], price: float
    ) -> float:
        if not price or not order_side:
            return 0
        # Sell order
        if order_side == 'sell':
            return await self.get_currency_balance(self.currency_pair.get_base())
        # Buy order
        amount = await self.get_currency_balance(self.currency_pair.get_quote())
        if amount == 0:
            return 0
        amount = amount / price
        market = self.api.markets[self.currency_pair.get_symbol()]
        amount = decimal_to_precision(amount, TRUNCATE, market['precision']['amount'])
        return float(amount)
