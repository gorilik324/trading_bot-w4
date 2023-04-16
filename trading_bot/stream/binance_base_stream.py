import json
import time
from abc import ABC

import websockets

from exchange_extra.currency_pair import CurrencyPair
from trading_bot.stream.stream_base import StreamBase


class BinanceBaseStream(StreamBase, ABC):
    def __init__(self, stream_name: str = None, currency_pair: CurrencyPair = None  ):
        # if stream_name is None use stream_name from class if it exists, else raise error
        if stream_name is None:
            if self.stream_name is not None:
                stream_name = self.stream_name
            else:
                raise ValueError("Stream name must be specified")
        super().__init__(stream_name=stream_name, currency_pair=currency_pair)
        self.id = int(str(int(time.time()))[-10:])
        self.stream_url = f"wss://stream.binance.com:9443/ws/{self.currency_pair.get_lowercase()}@{self.stream_name}"

        self.websocket = None

    async def subscribe(self) -> None:
        try:
            async with websockets.connect(self.stream_url) as websocket:
                self.websocket = websocket
                # Construct the JSON-RPC request
                request = {
                    "method": "SUBSCRIBE",
                    "params": [f"{self.currency_pair.get_lowercase()}@{self.stream_name}"],
                    "id": self.id
                }

                await websocket.send(json.dumps(request))

                # Start listening for incoming messages
                async for message in websocket:
                    data = json.loads(message)
                    for listener_fn in self.listeners:
                        await listener_fn(data)

        except Exception as e:
            print(f"Error occurred with `{self.stream_name} stream`: {e}")

    # Close the stream
    async def unsubscribe(self) -> None:
        # send an unsubscribe message to the stream
        unsubscribe_message = {
            "method": "UNSUBSCRIBE",
            "params": [f"{self.symbol}@{self.stream_name}"],
            "id": self.id
        }
        await self.websocket.send(json.dumps(unsubscribe_message))
        await self.websocket.close()
