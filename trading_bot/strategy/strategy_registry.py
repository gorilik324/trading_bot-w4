from typing import Dict, Type

from trading_bot.strategy.base_strategy import BaseStrategy
from trading_bot.strategy.depth_strategy import DepthStrategy


STRATEGY_REGISTRY: Dict[str, Type[BaseStrategy]] = {
    'depth_strategy': DepthStrategy,
}
