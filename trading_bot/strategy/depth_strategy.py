"""
This strategy works by connecting to the Binance websocket stream and
listening for updates in the order book for the BTC/TUSD pair.
The strategy takes the current price (let's call it x) and compares it to the difference
between the volume of buy orders (at a price from x to x-0.01%),
the volume of sell orders (at a price from x to x+0.01%). If the difference between these volumes is 70%/30% or more,
then an order is created.
If the volume is larger for buying, then the order for buying, if larger for selling, then for selling.
As soon as the order was executed, the order is immediately created in the reverse order,
taking into account the margin.
The strategy also checks the status of an open buy order and cancels it if it has been open for too long.
The goal of this strategy is to profit from small price fluctuations in the market.
"""
import random
from typing import Dict, List

import ccxt
import redis

import trading_bot.exchange_extra.depth as depth
from trading_bot.exchange_extra.currency_pair import CurrencyPair
from trading_bot.strategy.base_strategy import BaseStrategy
from trading_bot.stream.stream_manager import StreamManager


class DepthStrategy(BaseStrategy):
    def __init__(self, currency_pair: CurrencyPair, api: ccxt.Exchange, redis_client: redis.Redis,
                 stream_manager: StreamManager):
        super().__init__(currency_pair, api, redis_client, stream_manager)
        self.name = 'depth'
        self.stream_manager.add_stream('depth', self.currency_pair)
        self.stream_manager.add_listener('depth', self.on_stream_data_update)

    async def start(self):
        pass

    async def trade(self, depth_data: Dict[str, List[Dict]]) -> None:
        bids = depth.get_bids(depth_data)
        asks = depth.get_asks(depth_data)
        if not bids or not asks:
            return None

        MARGIN_PERCENTAGE = round(random.uniform(55, 75), 2)
        DEPTH_PERCENTAGE = round(random.uniform(0.005, 0.02), 3)
        ORDER_TIMEOUT = round(random.uniform(15, 60), 0)

        # TODO: handle partial filled orders,
        #  specially when the buy order is partially filled and the price changes

        active_orders = self.order_manager.get_open_orders()
        if len(active_orders) == 0:
            # Create order if there is no open order, or if the order has been closed.
            # The order is created in the direction of the larger volume.
            order_side = depth.get_order_side(bids, asks, MARGIN_PERCENTAGE, DEPTH_PERCENTAGE)
            if not order_side:
                return None

            price = depth.get_lowest_price(order_side, bids, asks)
            await self.order_manager.create_order(order_side, price)
        else:
            # Cancel order if it has been open for too long
            for active_order in active_orders.values():
                await self.order_manager.cancel_order_if_timeout(active_order, ORDER_TIMEOUT)
                break

            if self.order_manager.data['status'] == 'closed':
                # Create order in the opposite direction
                order_side = 'buy' if self.order_manager.data['side'] == 'sell' else 'sell'
                price = depth.get_lowest_price(order_side, bids, asks)
                await self.order_manager.create_order(order_side, price)
                # TODO: Add logic for when the order is partially filled or not filled at all
                self.order_manager.data = None

    async def on_stream_data_update(self, data: Dict[str, List[Dict]]) -> None:
        """
        This function is called every time there is an update to the order book on the Binance exchange.
        It checks the current order book and creates an order if the conditions for the strategy are met.
        """
        await self.trade(data)
