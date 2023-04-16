from exchange_extra.currency_pair import CurrencyPair
from stream.binance_base_stream import BinanceBaseStream


class BinanceDepthStream(BinanceBaseStream):
    def __init__(self, stream_name: str = None, currency_pair: CurrencyPair = None):
        self.stream_name = "depth"
        super().__init__(stream_name=stream_name, currency_pair=currency_pair)
