# Binance Trading Bot
A simple trading bot for the Binance cryptocurrency exchange, implementing a specific trading strategy. This project uses Python, the CCXT library, and Docker for easy setup and deployment.

## Trading Strategy
The trading bot operates on the BTC/TUSD trading pair, because of [Zero-Fee](https://www.binance.com/en/support/announcement/updates-on-zero-fee-bitcoin-trading-busd-zero-maker-fee-promotion-be13a645cca643d28eab5b9b34f2dc36).
It is using the following strategy:

1. Buy BTC at the lowest price in the last 3 minutes.
2. Sell BTC with a 0.2% margin.

## Technologies
- Python: The trading bot is implemented in Python.
- CCXT: The CCXT library is used for interacting with the Binance API.
- Docker: Docker is used for containerization, ensuring a consistent environment across different platforms.

## Running the Project Locally

### Prerequisites
- Docker: Install Docker from the official [website](https://www.docker.com/get-started/).

### Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/andrewhorokhovets/trading_bot.git
    cd trading_bot
    ```
2. Create a .env file in the app/ directory:
    ```bash
    cp config/.env.example config/.env
    ```
3. Open the .env file with a text editor and add your [Binance API key and secret key](https://www.binance.com/en/support/faq/how-to-create-api-360002502072):
    ```markdown
    BINANCE_API_KEY=your_api_key
    BINANCE_SECRET_KEY=your_secret_key
    ```
4. Run the Docker container:
    ```bash
   docker-compose up --build
    ```

The trading bot will now start executing trades according to the specified strategy.

## Useful commands
- SSH to docker container.
   ```bash
     docker exec -it trading_bot_instance /bin/bash
   ```
   