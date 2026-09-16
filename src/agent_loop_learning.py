

from google import genai
from google.genai import types
import os
import time
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

start = time.perf_counter()

response = client.models.generate_content_stream(
    model="gemini-3.8-flash",
    contents="2 + 2",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_level="low"
        )
    )
)


# types  explore and implement in the tool_response , 