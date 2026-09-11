

# microphone → audio bytes/file

'''
Microphone
    ↓
PCM audio chunks    
    ↓
Deepgram Flux (WebSocket)
    ↓
live transcript
    ↓
Gemini agent

'''

 #? Whats this PCM audio chunks ?? 

'''
#? PCM-> Pulse Code Modulation

Exactly. The key thing to understand is that PCM audio is not text. It is the raw numerical 
representation of the sound coming from your microphone.

'''

# Step1:
# Capturing Sound: A microphone uses a diaphragm to turn sound waves into a continuous, analog electrical signal.

# Step2:
# An ADC (analog-to-digital converter, usually handled by your OS/browser) samples that wave thousands of times per second

# Step3
# Each sample is stored as a number representing the amplitude at that instant

# Step4
# These numbers, one after another, are the "PCM chunks" flowing in your pipeline

'''
Key parameters that define a PCM chunk:

1.Sample rate — how many samples per second (e.g., 16000 Hz = 16000 samples/sec). Deepgram Flux typically 
expects 16kHz.

2.Bit depth — how much precision per sample (commonly 16-bit)

3.Channels — mono (1) or stereo (2). Voice pipelines almost always use mono.

4.Chunk size — you don't send one giant stream; you send it in small slices (e.g., 20-50ms of audio at a time)
so it can be streamed in near real-time over the WebSocket.


'''


#? why PCM chunks

'''
Why PCM specifically (not mp3/opus/etc.) — it's uncompressed, so there's zero decoding delay or artifact risk
 before Deepgram processes it. Speed matters more than file size here.
'''

#? Are there other chunks besides PCM ?? 

'''
Yes — any codec can be chunked and streamed:

PCM chunks (raw samples)
Opus chunks (compressed frames, e.g. 20ms each — this is WebRTC's default)
MP3 frames (less common for live streaming, more for files)

'''

#? Deepgram Nova-3
'''
Deepgram Flux — accepts raw PCM (linear16) directly, no decode step needed on their end. This is why most 
real-time STT pipelines use PCM: zero decode latency, simplest wire format, no codec compatibility headaches.

'''

#? Why PCM ?? 

'''

No decode step needed on their end. This is why most real-time STT pipelines use PCM: zero decode latency, 
simplest wire format, no codec compatibility headaches

'''




'''
#? pipeline: 

mic → OS captures raw waveform → sliced into small PCM chunks → 
each chunk pushed over the WebSocket to Deepgram Flux → Flux streams back partial/final transcripts → 
those go to your Gemini agent as text.

'''

#? Whats encoding/ decoding here ??

# In this case when we say encoding it meqans compressing the data from raw PCM samples to compressed forms
# like opus / mp3 






 #? Learn Websocket implementation here ,

