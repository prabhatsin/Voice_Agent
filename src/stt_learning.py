


# audio → text



#? What is ffmpeg ??
'''
FFmpeg stands for Fast Forward Moving Picture Experts Group. 

It is a free, open-source command-line tool and framework used to process video, audio, and other 
multimedia files and streams.

'''


'''
                 STEP 1
Microphone → Deepgram STT
                 ↓
              text
                 ↓
            Gemini Agent
                 ↓
              text
                 ↓
               TTS

'''

'''
STEP 2 → streaming STT
STEP 3 → streaming TTS
STEP 4 → interruption / barge-in
STEP 5 → VAD
STEP 6 → latency optimization
STEP 7 → observability
STEP 8 → deployment

'''


'''
Deepgram has broadly two relevant approaches:

#?1.STT API → audio → text (you build the agent yourself).

#?2.Voice Agent API → combines STT + LLM + TTS + voice-agent features.


For your project, we should use STT API first, because you're building the 

agent architecture yourself.

'''





import os
from dotenv import load_dotenv
from deepgram import AsyncDeepgramClient
import asyncio
load_dotenv()

API_KEY = os.getenv("DEEPGRAM_API_KEY")

client=AsyncDeepgramClient(api_key=API_KEY)

# SDK automatically uses /v2/listen endpoint
async with client.listen.v2.connect(
    model="flux-general-en",
    encoding="linear16",
    sample_rate=16000,
    request_options={
        "additional_query_parameters":{
            "language_hint":["en","es"],
        }
    },
) as connection:

    # Your code here

    pass






'''

audio.py's only job: mic → PCM chunks. It doesn't know Deepgram exists.

# The Flux connection code is a separate piece that:

1.Sends — pulls chunks from audio.py's generator, forwards them to Deepgram
2.Receives — listens for transcript events coming back from Deepgram on that same socket
3.Forwards that transcript text onward to your Gemini agent loop

'''
#? The full chain is 
'''

audio.py (mic → PCM) → Flux connection (send PCM, receive transcript) → Gemini agent (receives transcript, 
decides response )

'''

















'''

Deepgram Flux is a speech-to-text model that combines transcription + turn-detection into one model,
built specifically for voice agents (not general transcription).


The core problem it solves:

->Traditional STT pipelines (like Nova-3 + separate VAD(Voice Activity detector) are two disconnected systems:

->audio → STT (transcribes words) → separate silence-detector (guesses when user stopped talking)



#?
In short: Nova-3 = "transcribe what was said." Flux = "transcribe and tell you when it's your turn to 
espond" — purpose-built for the exact voice-agent turn-taking problem you're building toward.


'''