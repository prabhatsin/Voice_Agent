
# #? This file : handles microphone input → raw PCM audio chunks, which we then stream to Deepgram.

import sounddevice as sd

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
    ) as stream:

        print("🎤 Microphone started...")

        while True:
            data, overflowed = stream.read(CHUNK_SIZE)

            if overflowed:
                print("⚠️ Audio buffer overflow")

            yield data


if __name__ == "__main__":
    for chunk in audio_stream():
        print(len(chunk))























#? Explore , .wav file , .mp3, .flac what are they and the difference 
