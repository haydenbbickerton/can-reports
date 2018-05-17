#
# I made this script as a middleman between redis and websockets.
# Whenever the redis insance gets a message on the "canreports" channel,
# It get's sent to the client via websocket.
#
import os
import asyncio
import aioredis
import websockets

async def main(websocket, path):
    print('listening for redis')
    sub = await aioredis.create_redis(('redis', os.getenv('REDIS_PORT')))
    res = await sub.subscribe('canreports')
    ch1 = res[0]

    async def async_reader(channel):
        while await channel.wait_message():
            message = await channel.get(encoding='utf-8')
            if message is "EXIT":
                break

            await websocket.send(message)  # Send the message to the client

    try:
        task = asyncio.ensure_future(async_reader(ch1))  # assign listener on the channel
        await task
        sub.close()
    except websockets.exceptions.ConnectionClosed as e:
        print(repr(e))

if __name__ == '__main__':
    start_server = websockets.serve(main, '0.0.0.0', os.getenv('REALTIME_PORT'))
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(start_server)
        loop.run_forever()
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()