import logging
import re
import sys

from telethon import TelegramClient, events
from telethon.tl.types import PeerChannel

from qx_broker_automation_script import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.getLogger().setLevel(logging.WARNING)
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.WARNING)

telegram_api_id = 27224311
telegram_api_hash = '9c11a1bcad7528b43b07fbf454a83549'
qx_bot_update = 'https://t.me/qx_bot_updates'
test_channel = 'https://t.me/manoj_5047'
session_name = 'ALL-CHATS'
qx_signal_channel_name = 'Trading BTC Signals'
my_channel_name = 'Test'

client = TelegramClient(session_name, telegram_api_id, telegram_api_hash)


# @client.on(events.NewMessage(chats='wolfxsignals'))
# async def my_event_handler(event):
#     logging.debug(event.message)


#     # Replace this with your own code to handle the incoming messages

def get_future_time_in_seconds():
    now = datetime.datetime.now()
    return now.strftime('%H:%M:%S.{}').format(now.microsecond // 1000)


async def get_future_time_in_seconds_await():
    now = datetime.datetime.now()
    return now.strftime('%H:%M:%S.{}').format(now.microsecond // 1000)


async def place_order(order_time, direction, amount):
    if direction == 'UP':
        place_long_order(True, order_time, amount)

    elif direction == 'DOWN':
        place_short_order(True, order_time, amount)

    try:
        time_in_seconds = get_future_time_in_seconds()
        await send_message_to_group(f"Placed Order on {direction} with {amount}$ for {order_time} at {time_in_seconds} "
                                    , qx_bot_update)
    except:
        logger.error('Error in telegram sending.')


def stop_trading():
    close_browser()


@client.on(events.NewMessage())
async def handle_new_message(event):
    logger.debug(f'{get_future_time_in_seconds()} :: Received Msg')
    if event.message:
        if event.chat.title == qx_signal_channel_name or event.chat.title == my_channel_name:
            match = re.compile(r'put “(UP|DOWN)”').search(event.message.message)
            if match:
                await place_order(order_time=5, direction=match.group(1), amount=1)
                logger.debug(f'{get_future_time_in_seconds()} : The value is {match.group(1)}.')
                logger.debug(f'{get_future_time_in_seconds()} :: Group title ==> {event.chat.title}')

            else:
                text = event.message.message
                info = re.search(r'\b(WIN|DEAL)\b', text)
                if info is not None:
                    value = info.group(0)
                    logger.debug(f'{get_future_time_in_seconds()} : The trade status is {value}.')
                    await send_message_to_group(f"Order status {value}", qx_bot_update)

                else:
                    logger.error(f'{get_future_time_in_seconds()} :: Unsupported Message ==> {event.message.message}')
        else:

            logger.error("Different MESSAGE from different group" + f'${event.chat.title}' + f'${event.message}')

    if event.message.message is not None:
        await send_message_to_group(event.message.message, None)


async def send_message_to_group(messages, group_id):
    try:
        # Find your group by its username or ID
        group_entity = await client.get_entity(test_channel if group_id is None else group_id)
        # Send your message
        await client.send_message(PeerChannel(group_entity.id.real), messages)
    except:
        logger.error('Error in sending Message')


async def start_client():
    start_driver()
    if login_flow_script():
        await client.start()
        await client.run_until_disconnected()
    else:
        logger.error("Login Failed")
        sys.exit()


if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(start_client())
