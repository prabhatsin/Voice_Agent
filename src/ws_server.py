
import asyncio
import websockets


async def handler(websocket):
    print("client_connected")

    # while True:
    #     message = await websocket.recv()
    async for message in websocket:
        print("Client:", message)
        await websocket.send("Received: "+ message)



async def main():
    async with websockets.serve(handler,"localhost",8765): #websockets.serve(handler, host, port, **kwargs)

        #8756 is the default port used by pythons websocket library , its not the standadr default port 
        #Real default ports (80/443) only apply when you don't specify a port at all and rely on the standard ws:// or wss:// scheme resolution
        print("Server running...")
        await asyncio.Future()  # run forever


asyncio.run(main())





#? Question : Whats this 'websocket' argument in the handler function ?? and how can  it do websocket.send() 
#? and all this , also can we name it antything random or just websocket ??


'''
# When the WebSocket library calls your 'handler',it automatically passes a WebSocket connection object into it
# when handler is passed into ' websockets.serve(handler,"localhost",8765)' ,the websockets library creates 
  a WebSocket connection object and passes that object to your function.

# You start the server, async with websockets.serve(handler, "localhost", 8765):

"Start a WebSocket server, and whenever a client connects, use my handler function."

# As per the naming convention , u can it anything 'websocket' or 'connection' or anything

#! conclusion
#! websocket is referring to that WebSocket connection object created by the library.

'''

#? Question whats this async for loop , i have used normal for loop

'''
#!. Normal for

Suppose:

numbers = [10, 20, 30]

for number in numbers:
    print(number)

Python already has all the values:

numbers
   ↓
[10, 20, 30]
 ↓   ↓   ↓
10  20  30

So it can immediately do:

get 10 → process
get 20 → process
get 30 → process

#!. But imagine the values aren't available yet

Imagine someone says:

"I'll give you a number, but I don't know when the next number will arrive."

For example:

number 1 → now
number 2 → 2 seconds later
number 3 → 5 seconds later
number 4 → 1 second later
...

You can't use a normal list:

for number in numbers:

because the numbers don't exist yet.

You need to wait asynchronously for each next value.

That's where:

async for

comes in.

#! Mental model

Normal for:

for item in collection:

    "Give me the next item"
    ↓
    immediately available

async for:

async for item in async_source:

    "Give me the next item"
    ↓
    ⏳ wait asynchronously if necessary
    ↓
    item arrives
    ↓
    execute body


'''



# async def = "this function, when called, gives you a coroutine object"

#?Question: Why are we using , async with , not normal with ??? -------------------------------------------------------------


'''

1.We are NOT using async with just because we're inside an async def function. Being inside async def is a 
requirement (you're only allowed to use async with/await there), but it's not the reason you use it.


2.The actual reason is: websockets.serve() returns an object that is an asynchronous context manager — meaning 
its setup (__aenter__) and teardown (__aexit__) are coroutines that need awaiting internally 
(because starting/stopping a server involves I/O).



So the logic chain is actually:

i) websockets.serve() needs to do async work to start/stop → so it's built as an async context manager
ii) Because it's an async context manager, you must use async with to work with it
iii) Because async with involves awaiting internally, it can only be used inside an async def function


'''


'''
#?-------------------------------
1.async with is used for asynchronous context managers — objects whose setup and teardown logic involves 
await-able operations, instead of plain synchronous ones.

#!Normal with:

with open("file.txt") as f:
    ...

Here, open() returns an object with regular __enter__ and __exit__ methods — no waiting involved, just plain function calls.


#!async with:

async with websockets.serve(handler, "localhost", 8765):
    ...

Here, websockets.serve(...) returns an async context manager — an object with __aenter__ and __aexit__ methods, which are coroutines. That's because:

Entering it means actually starting the server — binding a socket, beginning to listen for connections. That's an I/O operation, so it needs await under the hood.
Exiting it means gracefully shutting the server down — closing all connections, which is also I/O and needs to be awaited.

'''



#? Why are we using asyncio.future ,?? 

'''
async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("Server started")

asyncio.run(main())


Here's what actually happens:

1.__aenter__ runs → server starts, binds to port 8765, begins listening

2. print("Server started") runs — one line, instantly done

3. There's nothing else in the block → Python immediately falls through to the end

4. __aexit__ runs → server shuts down, stops listening

5. main() returns → asyncio.run(main()) finishes → program exits




All of this happens in a fraction of a millisecond. The server technically "started," but no client would 
ever get the chance to connect, because it's already shut down by the time you'd try.

#!The fix: put something in the block that never finishes

asyncio.Future() creates a bare Future object — a placeholder for a result that hasn't happened yet. 
Nothing in this code ever calls .set_result() on it, so:

i)await asyncio.Future() pauses execution right there, forever (or until the program is killed).
ii) Because execution is paused inside the async with block (not past it), __aexit__ never gets triggered.
iii) The server keeps running indefinitely, because the block never "finishes" in the normal sense.


#! Alternative :

async def main():
    server = await websockets.serve(handler, "localhost", 8765)
    await server.wait_closed()

Here,server.wait_closed() is itself a Future-like awaitable that only resolves once someone calls server.close()
'''

#? asyncio.run()
'''
What it does internally (step by step)

1.Creates a new event loop — the thing that actually schedules and runs coroutines, handles I/O, timers, etc.
2.Runs your coroutine (main()) on that event loop until it completes
3.Cancels any remaining tasks that are still pending when main() finishes (cleanup)
4.Shuts down async generators properly
5.Closes the event loop
6.Returns whatever value main() returned (or raises whatever exception it raised)

'''


#? await vs scheduled 

'''
Quick mental model

1.await x → "Do this now, and I'll wait right here until it's done."

2.asyncio.create_task(x) → "Start this now in the background, I'll check back on it later."

3.asyncio.gather(a(), b(), c()) → shorthand for creating tasks for a(), b(), c() all at once, and 
awaiting all of them together (runs them concurrently, returns when all are done).

'''


#? Question: There is this confusion about the , event loop , program ,, who is incharge of what  ??? 


'''

1.You define coroutines and decide when to schedule them (via create_task, gather, etc.)
2.The event loop (not you, not magic) decides which ready coroutine runs next, automatically,
 whenever one is paused/waiting
3."Elsewhere" = other coroutines that YOU already scheduled, sitting in the event loop's queue, 
waiting for their turn

It's not auto-detected in a mystical sense — it's a very mechanical process.



The event loop is like a single-threaded manager juggling a to-do list. You add things to the list
(create_task). Whenever something pauses itself (await ... sleep/recv/send), the manager looks at 
the list and picks the next ready thing to run. You don't micromanage when exactly — you just decide 
what goes on the list and when you personally need to wait for something (await).



'''


#?Question :"In async Python, I've noticed a common pattern: instead of calling asyncio.run(abcd()) directly 
#? on the function I actually want to run, there's usually a wrapper — async def main() — which awaits abcd()
#?  inside it, and that main() is what actually gets passed to asyncio.run(). Is this just a convention, or 
#? is there a technical reason asyncio.run() isn't called directly on the function I care about?"


'''
Yes, that's absolutely true — it's the standard convention, not a strict technical requirement, but there are 
solid reasons behind it.


#! 1. asyncio.run() should only be called once

As mentioned earlier, asyncio.run() is meant to be your program's single entry point. If you have multiple 
async functions you need to run, you can't do:

asyncio.run(abcd())
asyncio.run(efgh())
asyncio.run(ijkl())

#!---->
=> Well, you technically can — but each call creates a brand new event loop, runs it, and tears it down. 
That's wasteful and breaks things if these functions need to share state, run concurrently, or depend on 
each other.


So the convention is: wrap everything in one main(), and call asyncio.run(main()) once.


#! 2. main() acts as an orchestrator/composition point

Real async programs usually need to run multiple coroutines — sometimes sequentially, sometimes concurrently.
 main() is where you decide how they relate to each other:


async def main():
    # sequential
    result1 = await abcd()
    result2 = await efgh(result1)

    # OR concurrent
    results = await asyncio.gather(abcd(), efgh(), ijkl())

    # OR fire-and-forget background tasks
    task = asyncio.create_task(background_worker())


        
You can't express this kind of orchestration logic outside of an async def function, because await, 
asyncio.gather(), asyncio.create_task(), etc. all require being inside a running event loop / coroutine 
context.

The main() pattern becomes valuable specifically when:

1.You have multiple coroutines to coordinate
2.You need setup/teardown logic (e.g., open a DB connection, then run server, then close connection)
3.You want structured error handling in one place
4.The program has any real complexity beyond "run one thing"

'''