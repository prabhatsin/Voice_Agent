import asyncio
import websockets





async def send_message(websocket):
    while True:
        message=input("you: ")
        await websocket.send(message)


async def main():

    async with websockets.connect("ws://localhost:8765") as websocket:
        print("connected to server")

        asyncio.create_task(send_message(websocket))


        # we want our main() to be alive , because if main() reaches the end , connection closes and program exits
        # and in this case we want concurrent communication 
        await asyncio.Future()

asyncio.run(main())

