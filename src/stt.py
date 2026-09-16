# this part lives in a third file , which uses 
from audio import audio_stream

async def send_audio(connection):
    for chunk in audio_stream(): # from audio.py
        await connection.send(chunk) # into the Websocket

#------------------------------------------------------------------

#TODO: cache-aware streaming--> Look  at the pinned chat 


