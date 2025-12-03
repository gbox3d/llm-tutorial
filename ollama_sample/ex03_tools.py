#%%
import ollama
from ollama import ChatResponse


MODEL = 'qwen3-vl:2b'  # tool calling 지원되는 모델

print(f"Using model: {MODEL}")

#%%
def add_two_numbers(a: int, b: int) -> int:
    return int(a) + int(b)

def subtract_two_numbers(a: int, b: int) -> int:
    return int(a) - int(b)

subtract_two_numbers_tool = {
    'type': 'function',
    'function': {
        'name': 'subtract_two_numbers',
        'description': '두개의 숫자를 입력받아 빼는 함수',
        'parameters': {
            'type': 'object',
            'required': ['a', 'b'],
            'properties': {
                'a': {'type': 'integer', 'description': 'The first number'},
                'b': {'type': 'integer', 'description': 'The second number'},
            },
        },
    },
}

add_two_numbers_tool = {
    'type': 'function',
    'function': {
        'name': 'add_two_numbers',
        'description': 'Add two numbers',
        'parameters': {
            'type': 'object',
            'required': ['a', 'b'],
            'properties': {
                'a': {'type': 'integer', 'description': 'The first number'},
                'b': {'type': 'integer', 'description': 'The second number'},
            },
        },
    },
}

tools = [add_two_numbers_tool, subtract_two_numbers_tool]

messages = [
    {'role': 'user', 'content': '10 빼기 2는 얼마야?'}
]

print("Prompt:", messages[0]['content'])

#%%
# LLM에게 요청 보내기 (function calling)
response: ChatResponse = ollama.chat(
    model=MODEL,      
    messages=messages,
    tools=tools
)

print("\n=== LLM Raw Response ===")
print(response)

#%%

# 🔥 추론(Reasoning)만 따로 뽑아서 출력
print("\n=== LLM Thinking ===")
print(response.message.thinking)   # ← 여기!

#%%
if response.message.tool_calls:
    print("\n=== Tool Call Detected ===")
    print(response.message.tool_calls)
    tool_call = response.message.tool_calls[0]
    
    print(f"name of tool to call: {tool_call.function.name}")
    print(f"arguments of tool to call: {tool_call.function.arguments}")
    
    fn_name = tool_call.function.name
    args = tool_call.function.arguments
    
    if fn_name == "add_two_numbers":
        result = add_two_numbers(**args)
    elif fn_name == "subtract_two_numbers":
        result = subtract_two_numbers(**args)
    else:
        raise ValueError("알 수 없는 함수 호출")
    
    print(f"\n=== Tool Call Result ===\n{result}")

    

# %%
