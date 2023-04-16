import asyncio
import os

import redis as redis
from dotenv import load_dotenv

import ccxt
from trading_bot.config import CURRENCY_PAIR
from trading_bot.exchange_extra.currency_pair import CurrencyPair
from trading_bot.trading_bot import TradingBot


async def main():
    load_dotenv('config/.env')
    api_key = os.environ['BINANCE_API_KEY']
    secret_key = os.environ['BINANCE_SECRET_KEY']
    exchange_name = os.environ['EXCHANGE_NAME']
    api = getattr(ccxt, exchange_name)({
        'apiKey': api_key,
        'secret': secret_key,
        'enableRateLimit': True
    })

    redis_host = os.getenv('REDIS_HOST')
    redis_port = 6379
    redis_db = 0
    redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

    currency_pair = CurrencyPair(CURRENCY_PAIR['base_currency'], CURRENCY_PAIR['quote_currency'])
    bot = TradingBot(currency_pair, api, redis_client)
    await bot.start()


if __name__ == '__main__':
    asyncio.run(main())
