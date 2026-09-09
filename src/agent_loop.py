
#? We will be using generate_content api

'''
Yes — generate_content is the low-level, stateless call where you fully control the contents array 
yourself (message history, roles, tool schemas, streaming flag)
'''
#TODO: after compleeting the agent loop , learn how to make it model/ llm agnostic

from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
from src.tool_schema import get_weather_function
from src.tools import get_weather
load_dotenv()
# api=os.getenv("GEMINI_API_KEY")

# def agent_loop():

client=genai.Client()
prompt="What's the weather in Delhi?"

weather_tool=types.Tool(function_declarations=[get_weather_function])

response=client.models.generate_content(
    model="gemini-3.8-flash",
    contents=prompt,
    config=types.GenerateContentConfig(
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=True
        ),
        tools=[weather_tool],
        thinking_config=types.ThinkingConfig(
            thinking_level='low'
        )
    )
)



# print(response.function_calls)

part=response.candidates[0].content.parts[0]
# print(part.function_call)
print(part.text)
tool_call=response.candidates[0].content.parts[0].function_call

if tool_call.name=='get_weather':
    result=get_weather(**tool_call.args)
    print("The temperature of Delhi is ",result)














# for chunk in response:
#     print(chunk)
#     # print(chunk.text,end="")








#? From the available reponse what are things that matter for us , ?? 

'''
1.

response
│
├── content.parts
│    ├── text            → model's answer
│    └── function_call   → model wants you to execute a tool
│
├── finish_reason        → why generation stopped
│
└── usage_metadata       → tokens / usage / later cost & performance analysis

2.
part.text
part.function_call

3.
LLM response
     │
     ├── function_call? ──→ execute tool ──→ call LLM again
     │
     └── text? ───────────→ final answer → STOP

'''
















#? what is AutomaticFUnctionCalling is ??

'''
With AFC enabled, the SDK essentially says:
1."Give me Python functions and I'll automatically execute the function and manage the call/response 
cycle."

2. By DEFGAULT AFC is enabled , in the SDK, 
3. Since we are building the agent wa want to have the control to execute the function ourself ,



             YOUR AGENT LOOP
                   │
                   ▼
              ┌─────────┐
              │ Gemini  │
              └────┬────┘
                   │
             function_call
                   │
                   ▼
              YOUR CODE
                   │
              execute tool
                   │
                   ▼
             function_result
                   │
                   ▼
              ┌─────────┐
              │ Gemini  │
              └────┬────┘
                   │
                   ▼
                answer

                
'''

