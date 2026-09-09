# # import time


# # from google import genai
# # import os
# # from dotenv import load_dotenv
# # load_dotenv()

# # api=os.getenv("GEMINI_API_KEY")
# # client=genai.Client()

# # start = time.perf_counter()

# # interaction = client.interactions.create(
# #     model="gemini-3.8-flash",
# #     input="2 + 2",
# #     generation_config={
# #         "thinking_level": "low"
# #     },
# #     stream=True
# # )

# # first_event = None
# # first_text = None

# # for event in interaction:

# #     now = time.perf_counter()

# #     if first_event is None:
# #         first_event = now
# #         print(
# #             f"First SSE event: {first_event - start:.3f}s"
# #         )

# #     if (
# #         event.event_type == "step.delta"
# #         and event.delta.type == "text"
# #     ):

# #         if first_text is None:
# #             first_text = now
# #             print(
# #                 f"First text: {first_text - start:.3f}s"
# #             )

# #         print(event.delta.text, end="", flush=True)

# # end = time.perf_counter()

# # print(f"\nTotal: {end - start:.3f}s")


# from google import genai
# import os
# import time
# from dotenv import load_dotenv

# load_dotenv()

# client = genai.Client()

# start = time.perf_counter()

# response = client.models.generate_content_stream(
#     model="gemini-3.8-flash",
#     contents="2 + 2",
# )

# first_text = None

# for chunk in response:

#     if chunk.text:

#         if first_text is None:
#             first_text = time.perf_counter()
#             print(
#                 f"TTFT: {first_text - start:.3f}s"
#             )

#         print(chunk.text, end="", flush=True)

# end = time.perf_counter()

# print(f"\nTotal: {end - start:.3f}s")

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

first_text = None

for chunk in response:
    if chunk.text:
        if first_text is None:
            first_text = time.perf_counter()
            print(f"TTFT: {first_text - start:.3f}s")

        print(chunk.text, end="", flush=True)

end = time.perf_counter()

print(f"\nTotal: {end - start:.3f}s")