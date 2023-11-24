#%%
import os
import time
import torch
from transformers import pipeline,AutoModelForCausalLM

from dotenv import load_dotenv
# .env 파일 로드 및 Pinecone 초기화
load_dotenv()


start_tick = time.time()
model_name ="beomi/llama-2-ko-7b"
# model_name ="beomi/KoAlpaca-Polyglot-12.8B"

pipe = pipeline(
    task="text-generation", 
    model=model_name, 
    tokenizer=model_name,
    torch_dtype=torch.float16,
    device_map="auto" # GPU 상황에 맞게 자동으로 설정
    # device_map="cuda:0"  # GPU 0사용 설정)
)

print(f'Load time: {time.time() - start_tick}')

def parse_text(data):
    for item in data:
        text = item['generated_text']
        text = text.replace('u200b', '')
        print(text +'\n\n') 

#%%
start_tick = time.time()
answer = pipe(
        """
        아래의 질문에 대한 답변해주세요.
        ### 질문 : 지구의 위성은 무엇이 있을까요?
        ### 답변 :
        """,
        do_sample=True,
        max_new_tokens=20,
        temperature=0.01,
        top_p=0.95,
        return_full_text=False,
        num_return_sequences=1,
        repetition_penalty=1.2,
    )
# print(answer)

print(f'Load time: {time.time() - start_tick}')

parse_text(answer)

# %%
