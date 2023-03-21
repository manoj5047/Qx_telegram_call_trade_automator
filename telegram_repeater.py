import re

from telethon import TelegramClient, events
from telethon.tl.types import PeerChannel

from quotexapi.stable_api import Quotex
from qx_broker_automation_script import *

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
#     print(event.message)


#     # Replace this with your own code to handle the incoming messages

def get_future_time_in_seconds():
    now = datetime.datetime.now()
    return now.strftime('%H:%M:%S.{}').format(now.microsecond // 1000)


async def get_future_time_in_seconds_await():
    now = datetime.datetime.now()
    return now.strftime('%H:%M:%S.{}').format(now.microsecond // 1000)


async def place_order(time, direction, amount):
    if direction == 'UP':
        place_long_order(True, time, amount)

    elif direction == 'DOWN':
        place_short_order(True, time, amount)

    try:
        time_in_seconds = get_future_time_in_seconds()
        await sendMessageToGroup(f"Placed Order on {direction} with {amount}$ for {time} at {time_in_seconds} ",
                                 qx_bot_update)
    except:
        print('Error in telegram sending.')


def stop_trading():
    closeBrowser()


@client.on(events.NewMessage())
async def handle_new_message(event):
    print(f'{get_future_time_in_seconds()} :: Received Msg')
    if event.message:
        if event.chat.title == qx_signal_channel_name or event.chat.title == my_channel_name:
            match = re.compile(r'put “(UP|DOWN)”').search(event.message.message)
            if match:
                # await place_order(time=5, direction=match.group(1), amount=1)
                print(f'{get_future_time_in_seconds()} : The value is {match.group(1)}.')
                print(f'{get_future_time_in_seconds()} :: Group title ==> {event.chat.title}')

            else:
                text = event.message.message
                info = re.search(r'\b(WIN|DEAL)\b', text)
                if info is not None:
                    value = info.group(0)
                    print(f'{get_future_time_in_seconds()} : The trade status is {value}.')
                    await sendMessageToGroup(f"Order status {value}", qx_bot_update)

                else:
                    print(f'{get_future_time_in_seconds()} :: Unsupported Message ==> {event.message.message}')
        else:

            print("Different MESSAGE from different group" + f'${event.chat.title}' + f'${event.message}')

    if event.message.message is not None:
        await sendMessageToGroup(event.message.message, None)


async def sendMessageToGroup(messages, groupId):
    try:
        # Find your group by its username or ID
        group_entity = await client.get_entity(test_channel if groupId is None else groupId)
        # Send your message
        await client.send_message(PeerChannel(group_entity.id.real), messages)
    except:
        print('Error in sending Message')


async def startClient():
    # await connectQXApi()
    # start_driver()
    # login_flow_script()
    await client.start()
    await client.run_until_disconnected()


async def connectQXApi():
    ssid = """42["authorization",{"session":"eyJpdiI6IjczRDdzUWtreG1NM01ZNUVkZHlmNkE9PSIsInZhbHVlIjoiWXpoN2ZoWjVFcVkzZ2YrS0RhNU84SG9rd0s0ZVJJazdXSUFMRURTN0tGajQxTFE2ZFlqci9","isDemo":1}]"""
    account = Quotex(set_ssid=ssid)
    check_connect, message = account.connect()
    print(check_connect, message)


if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(startClient())
