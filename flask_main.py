import asyncio

from flask import Flask

import telegram_repeater
from telegram_repeater import *

app = Flask(__name__)


@app.route('/')
def home():
    return 'Hello, world!'


@app.route('/start-client')
def start_client():
    print(get_future_time_in_seconds())
    asyncio.run(start_client())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888)

