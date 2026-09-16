
#!Note ; When using Livekit later we dont even have to write this audio.py file
# Purely for Learning purpose this is being written

# Right now:
# your audio.py (sounddevice) → raw PCM → your WebSocket code → Deepgram



# With LiveKit:

# LiveKit client SDK (browser/mobile/etc.) → LiveKit Room (WebRTC) → LiveKit Agent (Python, server-side)

'''
Not mandatory — you have full control.

Two separate layers, use what you want:

LiveKit transport layer (Room, WebRTC, media routing) — just moves audio in/out reliably
LiveKit Agents framework (Python, prebuilt STT/LLM/TTS plugins) — optional convenience wrapper

'''













#? This file : handles microphone input → raw PCM audio chunks, which we then stream to Deepgram.

import sounddevice as sd
# Library that talks to your OS's audio drivers to capture mic input.



'''

Overall: This code opens a live connection to your microphone and continuously reads small 80ms slices of 
raw audio (PCM, as we discussed) as they arrive — forever, in a loop — one chunk at a time.

Think of it like a tap that's always running: every 80ms, a fixed-size bucket of audio samples is ready, 
and you grab it.

'''
SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_DURATION = 0.08  # 80 ms

CHUNK_SIZE = int(SAMPLE_RATE * CHUNK_DURATION)

def audio_stream():
    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="int16",
        blocksize=CHUNK_SIZE,
        # tells the OS: "buffer up exactly 1280 samples before handing them to me."
    ) as stream:
    # with ... as stream — a context manager; it auto-opens the mic here and guarantees it's cleanly closed later (even on error/exit).
        print("🎤 Microphone started...")

        while True:
            data, overflowed = stream.read(CHUNK_SIZE)
            # data — the raw PCM bytes (your audio chunk)

            # overflowed — True if the OS buffer filled up faster than your code could read it (meaning you lost some audio — bad sign, means your loop is too slow).
            if overflowed:
                #Just warns you if that data loss happened.
                print("⚠️ Audio buffer overflow")

            yield data
            # Hands this chunk of audio out to whoever is looping over audio_stream(), then pauses right here — 
            # it doesn't restart the while loop until the 
            # caller asks for the next chunk (calls next() again, which a for loop does automatically).


if __name__ == "__main__":
    for chunk in audio_stream():
        print(len(chunk))



#? CHANNELS:

'''
A channel = one independent stream of audio samples.

1.Mono (1 channel) — one microphone signal, one sequence of numbers representing the sound wave. Every sample is just: volume at this instant.

2.Stereo (2 channels) — two separate signals, usually "left ear" and "right ear," captured by two mics (or engineered to sound like two mics) 
so a speaker/headphones can play slightly different sound in each ear, giving you a sense of directionality/space.


#For mono, one chunk of samples looks like:

[s1, s2, s3, s4, s5, ...]


#For stereo, samples are interleaved — left and right, alternating:

[L1, R1, L2, R2, L3, R3, ...]


#!Why your code uses mono (CHANNELS = 1):  ?? 

--> Your mic is capturing a person's voice for a voice agent. There's no "left ear / right ear" concept 
needed — you just need one clean signal of what they said. Using stereo would:

  double your data size for zero benefit
  possibly confuse the STT engine, which expects a single voice channel anyway

#? Music, movies, immersive audio → stereo (sometimes even more channels, like 5.1 surround). 


#? Voice capture / calls / STT → mono, almost always.

'''


#? CHUNKS

'''
In short: chunk size is a latency vs. efficiency tradeoff.

Smaller chunks → lower latency, higher overhead  ( trying to send 1 sample at a time , very highy network overahead )

Larger chunks → higher latency, lower overhead  ( trying to send all the samples in at once , )



Overhead — the extra "cost" (CPU time, network calls, processing) spent on managing the work, rather than doing
 the actual useful work itself. (Here: the cost of repeatedly calling functions and sending network packets, 
 separate from the actual audio data being transferred.)

'''
















#? Explore , .wav file , .mp3, .flac what are they and the difference 
