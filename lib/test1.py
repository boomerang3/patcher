import json
from llamaapi import LlamaAPI

def get_key(filename):
    try:
        with open(filename, 'r') as file:
            first_line = file.readline().strip()
            return first_line
    except FileNotFoundError:
        print(f"The file {filename} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

llama = LlamaAPI(get_key("keyLama.txt"))

api_request_json = {
    "model": "llama3.1-70b",
    "messages": [
        {"role": "user", "content": "What is the weather like in Boston?"},
    ],
    "functions": [
        {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "days": {
                        "type": "number",
                        "description": "for how many days ahead you wants the forecast",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
            },
            "required": ["location", "days"],
        }
    ],
    "stream": False,
    "function_call": "get_current_weather",
}

response = llama.run(api_request_json)
print(json.dumps(response.json(), indent=2))