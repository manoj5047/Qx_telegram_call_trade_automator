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

def get_future_time():
    # get the current time
    now = datetime.datetime.now()

    # add 5 minutes to the current time
    future_time = now

    # format the future time in HH:MM format
    future_time_str = future_time.strftime('%H:%M')

    # return the future time in HH:MM format
    return future_time_str


async def place_order(time, direction, amount):
    print("Placing order from Telegram")
    if direction == 'UP':
        place_long_order(True, time, amount)

    elif direction == 'DOWN':
        place_short_order(True, time, amount)

    await sendMessageToGroup(f"Placed Order on {direction} with {amount}$ for {time} Minutes", qx_bot_update)


def stop_trading():
    closeBrowser()


@client.on(events.NewMessage())
async def handle_new_message(event):
    if event.message:

        if event.chat.title == qx_signal_channel_name or event.chat.title == my_channel_name:
            print(f'{get_future_time()} :: Group title ==> {event.chat.title}')
            # print('Message ==> ' + f'{event.message.message}')
            text = event.message.message
            pattern = re.compile(r'put “(UP|DOWN)”')
            match = pattern.search(text)
            if match:
                value = match.group(1)
                print(f'{get_future_time()} : The value is {value}.')
                await place_order(time=5, direction=value, amount=1)
            else:
                info = re.search(r'\b(WIN|DEAL)\b', text)
                if info is not None:
                    value = info.group(0)
                    print(f'{get_future_time()} : The trade status is {value}.')
                    await sendMessageToGroup(f"Order status {value}", qx_bot_update)

                else:
                    print(f'{get_future_time()} :: Unsupported Message ==> {event.message.message}')
        else:

            print("Different MESSAGE from different group" + f'${event.chat.title}' + f'${event.message}')

    if event.message.message is not None:
        await sendMessageToGroup(event.message.message, None)


async def sendMessageToGroup(messages, groupId):
    # Find your group by its username or ID
    group_entity = await client.get_entity(test_channel if groupId is None else groupId)
    # Send your message
    try:
        await client.send_message(PeerChannel(group_entity.id.real), messages)
    except:
        print('Empty Message.')


async def startClient():
    # await connectQXApi()
    start_driver()
    login_flow_script()
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
