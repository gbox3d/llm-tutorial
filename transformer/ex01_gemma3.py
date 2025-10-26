#%%
from dotenv import load_dotenv
import os
import torch
from transformers import pipeline

load_dotenv('../.env')

# API 토큰을 가져옵니다.
token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
print(f'api-key : {token}')

#%%
pipe = pipeline(
    "text-generation",
    model="google/gemma-3-1b-it",
    device="cuda",
    torch_dtype=torch.bfloat16,
    token=token  # 인증 토큰 전달
)

#%%
messages = [
    [
        {
            "role": "system",
            "content": [{"type": "text", "text": "You are a helpful assistant."},]
        },
        {
            "role": "user",
            "content": [{"type": "text", "text": "Write a poem on Hugging Face, the company"},]
        },
    ],
]

output = pipe(messages, max_new_tokens=50)
print(output)

# %%

messages = [
    [
        {
            "role": "system",
            "content": [{"type": "text", "text": "당신은 능숙한 조력자입니다."},]
        },
        {
            "role": "user",
            "content": [{"type": "text", "text": "당신은 한국어 잘하시나요?"},]
        },
    ],
]

output = pipe(messages, max_new_tokens=50)
print(output)

# %%
