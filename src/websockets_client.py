import asyncio
import websockets


async def main():

    async with websockets.connect("ws://localhost:8765") as websocket:

        await websocket.send("Hello Server")
        print("Server:",await websocket.recv())

        await websocket.send("How are you")
        print("Server:",await websocket.recv())

        await websocket.send("Goodbye")
        print("Server:",await websocket.recv())

        
        # print("Connected to server")

asyncio.run(main())




# TOMMOROW:
# 1. aate hi understand 3 way handshake , \
# 2. more familiarity with websocket in Deepgram 

