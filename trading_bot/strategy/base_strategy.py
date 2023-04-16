import abc

import ccxt
import redis

from exchange_extra.order_manager import OrderManager
from trading_bot.exchange_extra.currency_pair import CurrencyPair
from trading_bot.stream.stream_manager import StreamManager


class BaseStrategy(abc.ABC):

    def __init__(self, currency_pair: CurrencyPair, api: ccxt.Exchange, redis_client: redis.Redis,
                 stream_manager: StreamManager):
        self.currency_pair = currency_pair
        self.api = api
        self.redis_client = redis_client
        self.stream_manager = stream_manager
        self.name = None
        self.order_manager = OrderManager(self.currency_pair, self.api, self.redis_client)

    @abc.abstractmethod
    async def start(self):
        pass

    def get_name(self):
        return self.name
