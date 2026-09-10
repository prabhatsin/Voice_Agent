
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
from src.tool_schema import get_weather_function,fehrenheit_temp
from src.tools import get_weather,fahrenheit_calculator
from src.tool_registry import tool_registry
load_dotenv()
# api=os.getenv("GEMINI_API_KEY")

# def agent_loop():

client=genai.Client()
# prompt="Give me the temperature of Nagpur in fahrenheit"

messages=[
    {"role":"user",
      "parts":[
          {
              "text":"Give me the temperature of Nagpur in fahrenheit"
          }
      ]
     }
]

print(messages)
while True:
    weather_tool=types.Tool(function_declarations=[get_weather_function])
    fahrenheit_tool=types.Tool(function_declarations=[fehrenheit_temp])
    response=client.models.generate_content(
        model="gemini-3.8-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=True
            ),
            tools=[weather_tool,fahrenheit_tool],
            thinking_config=types.ThinkingConfig(
                thinking_level='low'
            )
        )
    )
    parts=response.candidates[0].content.parts
    tool_call=None
    for part in parts:
        if part.function_call:
            tool_call=part.function_call
            #! This break statement takes out of the above for loop not the main while loop
            break
    if tool_call: # check if tool call present in the response
        print("MODEL RETURNED:.........")
        #step1:# 1. Append Gemini's model response containing the function call
        messages.append(response.candidates[0].content)
        print(response.candidates[0].content)
        print()
        print()

        # step2:Execute the actual Python function
        tool_name=tool_registry[tool_call.name]
        result=tool_name(**tool_call.args)


        # Step3: Append the functions result
        tool_response={
            "role":"tool",
            "parts":[
                {
                    "function_response":{
                        "name":tool_call.name,
                        "response":{
                            "result":result
                        }
                    }
                }
            ]
         
        }
        print("The response to be appended to the model is ",tool_response)
        messages.append(tool_response)

    else:
        print("No function call found in the response ")
        text_response={
            "role":"model",
            "parts":[
                {
                    "text":response.text
                }
            ]
        }
        print(text_response)
        messages.append(text_response)
        break











#? Question: You may wonder: Why is the function response role: "user" instead of "tool"?


'''
Because in Gemini's conversation protocol, the function response is represented as a part of the user-side
input back to the model. "tool" is your own conceptual label; it isn't the Gemini Content.role you're 
supposed to send here.

'''






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



#? Agent Loop in short

'''
while True:

    response = client.models.generate_content(...)

    part = response.candidates[0].content.parts[0]

    if part.function_call:
        # 1. Identify requested function
        # 2. Execute it
        # 3. Give result back to Gemini
        # 4. Continue loop

    else:
        # Final answer
        print(part.text)
        break

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

