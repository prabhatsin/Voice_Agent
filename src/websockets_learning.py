
#? Whats a socket then ?? 
# Socket = an endpoint through which a program sends and receives network data.

'''
Your Python program                         Another computer
      │                                           │
      │                                           │
   [Socket] ════════════════════════════════ [Socket]
'''
#  A socket is an OS-level communication endpoint associated with things such as:
# IP address
# Port
# Protocol....


#? Mistake to think that sockets are  only used in websocket , not http  ,??
#!Wrong.....

# HTTP uses sockets too. WebSocket uses sockets too.

# A socket isn't necessarily something that disappears when you switch protocols.


#? What is websocket ?? 

'''
WebSocket is a communication protocol that provides a persistent, two-way communication channel between a 
client and a server over a single connection. Unlike HTTP, where the client typically sends a request and 
waits for a response, with WebSocket both sides can send data whenever they need to. It's particularly useful
for real-time applications such as chat, live notifications, gaming, and streaming audio.
'''


 # ? How is it decided who is client and who is server because both can send and receive messages right ??


'''
1. Client/server describes the roles established when the connection is created, not who is allowed to send 
or receive data.

2.The client is the side that initiates the connection.

3.The server is the side that listens for incoming connections.

There is no rule saying:

->Client → can only send
->Server → can only receive


4.That's why WebSocket is called full-duplex (because Server can send,server can receive, and client can do 
both as well ?)

'''

#? Question ?? Mistake1. i thought , For a fastapi instance (suppose ) , one sever can handle only one client ?? 

#! Wrong ......

# point1: It depends on whether instance is asyncio implemented , single worker sync process , or thread implemented 

'''
1.One server instance can handle many clients even with synchronous code. However, with a single synchronous 
worker, requests are processed sequentially. 

2.Concurrency can be increased using multiple processes/workers, threads, or asynchronous I/O, depending on the architecture and workload.

'''

#? Mistake 2. I though if the process is completely sync ( no event loop, no threads then ),one sever can handle only one client ??


# Case 1: One worker + synchronous code
'''
                 FastAPI instance
                       │
                       │
                  Worker #1
                       │
             ┌─────────┴─────────┐
             ↓                   ↓
          Client A            Client B

'''
#So with one synchronous worker, yes:

#Only one request can be actively executing at a time(at a time is the important keyword here )

# But that's not the same as saying the instance can handle only one client.,The same instance can serve many clients sequentially.

'''
FastAPI is commonly run with Uvicorn.

You can run:

uvicorn main:app --workers 4

             FastAPI application
                     │
       ┌─────────────┼─────────────┐
       ↓             ↓             ↓
    Worker 1      Worker 2      Worker 3
                     ...

                     
--> Each worker is a separate process.

'''


#? TO EXPLORE MORE  IN DEPTH OF THIS , READ Must_Read.Docs --------->











'''
#? Your learning path

Do this:

#!Level 1 — Basic syntax

Understand:

connect
send
recv
close


#!Level 2 — Streaming

Understand:

while True
async for

 

#!Level 3 — Bidirectional communication

Build:

sender coroutine
receiver coroutine

running concurrently.

#!Level 4 — Binary data

Send:

bytes

instead of strings.

#!Level 5 — Real application

Then replace:

"Hello"

with:

PCM audio chunks

and replace our toy server with:

Deepgram Flux

That's the point where your current audio.py plugs directly into stt.py.

If you understand those 5 levels, you will be comfortable enough with WebSockets for this Voice AI project.

'''