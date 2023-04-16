from typing import Dict, Type

from trading_bot.stream.stream_base import StreamBase
from trading_bot.stream.binance_depth_stream import BinanceDepthStream

STREAM_REGISTRY: Dict[str, Type[StreamBase]] = {
    'depth': BinanceDepthStream
}
