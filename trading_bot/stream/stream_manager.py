import asyncio
from typing import Callable, List, Dict, Type

from exchange_extra.currency_pair import CurrencyPair
from stream.stream_base import StreamBase
from trading_bot.stream.stream_registry import STREAM_REGISTRY


class StreamManager:
    def __init__(self):
        self.streams: Dict[str, List[StreamBase]] = {}

    def get_stream_names(self):
        return dict.fromkeys(self.streams).keys()

    def add_stream(self, stream_name: str, currency_pair: CurrencyPair = None):
        if stream_name not in STREAM_REGISTRY:
            raise ValueError(f"Invalid stream name '{stream_name}' specified")
        if stream_name not in self.streams:
            stream_class: Type[StreamBase] = STREAM_REGISTRY[stream_name]
            stream_instance = stream_class(currency_pair=currency_pair)
            self.streams[stream_name] = [stream_instance]
        else:
            raise ValueError(f"Stream '{stream_name}' is already registered")

    def remove_stream(self, stream_name: str):
        if stream_name in self.streams:
            self.streams.pop(stream_name)
        else:
            raise ValueError(f"Stream '{stream_name}' is not registered")

    def stream_exists(self, stream_name: str):
        return stream_name in self.streams

    def add_listener(self, stream_name: str, listener_fn: Callable):
        if stream_name not in self.streams:
            raise ValueError(f"Stream '{stream_name}' is not registered")
        if listener_fn not in self.streams[stream_name][0].listeners:
            self.streams[stream_name][0].add_listener(listener_fn)

    def remove_listener(self, stream_name: str, listener_fn: Callable):
        if stream_name in self.streams and listener_fn in self.streams[stream_name][0].listeners:
            self.streams[stream_name][0].remove_listener(listener_fn)

    def notify_listeners(self, data: Dict[str, List[Dict]]):
        for stream_name in data:
            if stream_name in self.streams:
                for listener_fn in self.streams[stream_name][0].listeners:
                    listener_fn(data[stream_name])

    async def subscribe_all_streams(self):
        await asyncio.gather(*[stream[0].subscribe() for stream in self.streams.values()])
        print("Subscribed to all streams")

    async def unsubscribe_all_streams(self):
        await asyncio.gather(*[stream[0].unsubscribe() for stream in self.streams.values()])
        print("Unsubscribed from all streams")
