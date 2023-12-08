#%%
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer,pipeline

import time
import os
from dotenv import load_dotenv
# .env 파일 로드 및 Pinecone 초기화
load_dotenv()

# 모델과 토크나이저 초기화
model_name = "beomi/llama-2-ko-7b"

#%%
model_name = "beomi/llama-2-ko-7b"
print(f'Start loading {model_name}')

start_tick = time.time()

tokenizer = AutoTokenizer.from_pretrained(model_name)

hf_pipeline = pipeline(
    task="text-generation", 
    model=model_name, 
    tokenizer=tokenizer,
    torch_dtype=torch.float16,
    # load_in_8bit=True,
    # max_length=100, 
    # max_new_tokens=32,
    # temperature=0.1,
    do_sample=False,
    # repeat_penalty=1.15,
    # device_map="auto" # GPU 상황에 맞게 자동으로 설정
    device_map="auto"  # GPU 0사용 설정)
)

print(f'Load time: {time.time() - start_tick}')

model = hf_pipeline.model

#%%
def generate_text_interactively(prompt, max_length=50):
    # 입력 텍스트를 토큰으로 변환
    input_ids = tokenizer.encode(prompt, return_tensors="pt").to(model.device)

    # 생성된 텍스트를 저장할 변수
    generated = input_ids

    model.eval()
    with torch.no_grad():
        for _ in range(max_length):
            # 다음 토큰을 예측
            outputs = model(generated)
            next_token_logits = outputs.logits[:, -1, :]
            
            # 다음 토큰을 선택 (여기서는 가장 확률이 높은 토큰을 선택)
            next_token = torch.argmax(next_token_logits, dim=-1, keepdim=True)
            
            # 생성된 텍스트에 다음 토큰 추가
            generated = torch.cat([generated, next_token], dim=-1)

            # 다음 토큰을 텍스트로 변환하여 출력
            next_token_text = tokenizer.decode(next_token[0], skip_special_tokens=True)
            print(next_token_text)

            # 문장 종료 토큰이 생성되면 종료
            if next_token.item() == tokenizer.eos_token_id:
                break
#%%
# 예시 사용
prompt = "지구의 위성은 무엇이 있을까요?"
generate_text_interactively(prompt, max_length=20)
