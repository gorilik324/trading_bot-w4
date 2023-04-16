import asyncio
from typing import Dict

import ccxt
import redis as redis

from .config import STRATEGIES
from .exchange_extra.currency_pair import CurrencyPair
from .strategy.base_strategy import BaseStrategy
from .strategy.strategy_registry import STRATEGY_REGISTRY
from .stream.stream_manager import StreamManager


class TradingBot:
    def __init__(self, currency_pair: CurrencyPair, api: ccxt.Exchange, redis_client: redis.Redis):
        self.currency_pair = currency_pair
        self.api = api
        self.redis_client = redis_client
        self.stream_manager = StreamManager()

        # Initialize strategies
        self.strategies: Dict[str, BaseStrategy] = {}
        for strategy in STRATEGIES:
            if strategy not in STRATEGY_REGISTRY:
                raise ValueError(f"Invalid strategy '{strategy}' specified in config.py")
            strategy_cls = STRATEGY_REGISTRY[strategy]
            self.strategies[strategy] = strategy_cls(self.currency_pair, self.api, self.redis_client,
                                                     self.stream_manager)

    async def start(self):
        # Clear redis
        self.redis_client.flushdb()

        # Check that connection to exchange is successful
        self.api.load_markets()

        print(f"Starting trading bot for {self.currency_pair.get_symbol()}")
        await self.stream_manager.subscribe_all_streams()

        # Infinite loop to keep the event loop running
        while True:
            await asyncio.sleep(3600)
