import asyncio
import websockets

# from prompt_toolkit import PromptSession
# from prompt_toolkit.patch_stdout import patch_stdout

# session = PromptSession()

# async def send_messages(websocket):
#     while True:
#         message = await session.prompt_async("You: ")
#         await websocket.send(message)

# async def receive_messages(websocket):
#     async for message in websocket:
#         with patch_stdout():
#             print(f"Server: {message}")
#! The above code is to just fix the terminal output visually

async def send_messages(websocket):
    while True:
        message=await asyncio.to_thread(input,"You: ")
       
        await websocket.send(message)

async def receive_messages(websocket):
    async for message in websocket:
        print("\nServer:",message)


async def main():
    async with websockets.connect("ws://localhost:8765") as websocket:
        print("connected to server")
        asyncio.create_task(send_messages(websocket))
        # What does create_task does ??
        '''
        1.A Core Python function used to wrap a coroutine into a Task object and immediately schedule its execution concurrently within the running event loop.
        '''

        asyncio.create_task(receive_messages(websocket))
        # we want our main() to be alive , because if main() reaches the end , connection closes and program exits
        # and in this case we want concurrent communication 
        await asyncio.Future()

asyncio.run(main())


#! Learning : Normal input() is blocking in nature for the eventloop, it doesnt cooperate , it blocks the thread 

'''
1.input() is blocking. While you're sitting there typing/waiting for input, the asyncio event loop can stop 
processing WebSocket keepalive traffic

2.Next we'll replace input() with an async-friendly way of generating messages

'''



#? Question what is create_task() doing exactly , ???
'''
When you call asyncio.create_task(coro), Python does two things:

1.Schedules the coroutine: It submits the coroutine to the event loop to run "in the background". It will 
actually start executing the next time the event loop yields or hits an await point.

2.Returns a Task object: It gives you a handle (a subclass of Future). You can await this handle later
to retrieve the task's return value or to catch exceptions.

'''

