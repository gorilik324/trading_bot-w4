from abc import ABC, abstractmethod
from typing import Callable

from exchange_extra.currency_pair import CurrencyPair


class StreamBase(ABC):
    def __init__(self, stream_name: str = None, currency_pair: CurrencyPair = None  ):
        self.currency_pair = currency_pair
        self.stream_name = stream_name
        self.stream_url = None
        self.websocket = None
        self.listeners = []

    def get_stream_name(self) -> str:
        return self.stream_name

    def add_listener(self, listener_fn: Callable):
        self.listeners.append(listener_fn)

    @abstractmethod
    async def subscribe(self):
        pass
