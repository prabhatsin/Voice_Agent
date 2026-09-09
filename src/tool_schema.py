
get_weather_function={
    "name":"get_weather",
    "description":"Returns the current temperature for the specified city.",
    "parameters":{
        "type":"object",
        "properties":{
            "city":{
                  "type":"string",
                   "description":"The city whose current weather you want to know, e.g. Delhi."
            },
          
        },
        "required":["city"]
    }
}



