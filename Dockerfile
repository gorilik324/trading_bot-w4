# Use the official Python 3.9 slim image as a base.
FROM python:3.9.16-slim

# Set /trading_bot as the working directory inside the container.
WORKDIR /app

# Copy the requirements.txt file into the container.
COPY trading_bot/requirements.txt .

# Install the required packages using pip.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of project files into the container.
COPY config /app/config
COPY trading_bot /app/trading_bot
COPY main.py /app/

# Install redis-cli
RUN apt-get update && apt-get install -y redis-tools

# Keep the container running indefinitely without doing anything.
CMD tail -f /dev/null
