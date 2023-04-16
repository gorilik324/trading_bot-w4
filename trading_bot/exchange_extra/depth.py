from typing import Literal, List, Dict

from trading_bot.math_utils.arithmetic import Arithmetic


def get_highest_bid_price(bids: list) -> float:
    for bid in bids:
        if bid[1] > 0:
            return bid[0]


def get_lowest_ask_price(asks: list) -> float:
    for ask in asks:
        if ask[1] > 0:
            return ask[0]


# Sum up the volume of buy orders if the price is from lowest_ask_price to lowest_ask_price-0.01%
def get_sell_volume(asks: list, percentage=0.01):
    lowest_ask_price = get_lowest_ask_price(asks)
    highest_ask_price = Arithmetic.percent_increase(lowest_ask_price, percentage)

    buy_volume = 0
    for ask in asks:
        if ask[0] <= highest_ask_price:
            buy_volume += ask[1]
    return buy_volume


def get_buy_volume(bids, depth_percentage):
    highest_bid_price = get_highest_bid_price(bids)
    lowest_bid_price = Arithmetic.percent_decrease(highest_bid_price, depth_percentage)
    sell_volume = 0
    for bid in bids:
        if bid[0] >= lowest_bid_price:
            sell_volume += bid[1]
    return sell_volume


# Get preferred order type, based on the market's depth
def get_order_side(bids, asks, margin_percentage=50.01, depth_percentage=0.01) -> Literal['buy', 'sell', None]:
    if len(bids) == 0 or len(asks) == 0:
        return None

    buy_volume = get_buy_volume(bids, depth_percentage)
    sell_volume = get_sell_volume(asks, depth_percentage)

    sum_volume = buy_volume + sell_volume

    buy_volume_percentage = buy_volume / sum_volume * 100
    sell_volume_percentage = sell_volume / sum_volume * 100

    if buy_volume_percentage >= margin_percentage:
        return 'buy'
    elif sell_volume_percentage >= margin_percentage:
        return 'sell'

    return None


def get_bids(depth: Dict) -> List:
    if 'b' not in depth:
        return []
    return [[float(price), float(qty)] for price, qty in depth['b']]


def get_asks(depth):
    if 'a' not in depth:
        return []
    return [[float(price), float(qty)] for price, qty in depth['a']]


def get_lowest_price(order_side, bids, asks):
    if order_side == 'buy':
        return get_highest_bid_price(bids) + 0.01
    elif order_side == 'sell':
        return get_lowest_ask_price(asks) - 0.01

    return None
