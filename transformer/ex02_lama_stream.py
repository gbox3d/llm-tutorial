#%%
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

import time
import os
from dotenv import load_dotenv
# .env 파일 로드 및 Pinecone 초기화
load_dotenv()

# 모델과 토크나이저 초기화
model_name = "beomi/llama-2-ko-7b"
save_directory = "../../model_directory"  # 모델을 저장할 경로

model_save_directory = os.path.join(save_directory, model_name)

#%%
start_tick = time.time()
tokenizer = AutoTokenizer.from_pretrained(model_name)
# save_directory + / + model_name
tokenizer.save_pretrained(model_save_directory)
print(f"토크나이저 저장 완료: {model_save_directory} elapsed time: {time.time() - start_tick}")

model = AutoModelForCausalLM.from_pretrained(model_name).to('cuda' if torch.cuda.is_available() else 'cpu')
model.save_pretrained(model_save_directory)
print(f"모델 저장 완료: {model_save_directory}")

#%%
# 저장된 경로에서 모델과 토크나이저 로드
start_tick = time.time()
tokenizer = AutoTokenizer.from_pretrained(model_save_directory)
model = AutoModelForCausalLM.from_pretrained(model_save_directory).to('cuda' if torch.cuda.is_available() else 'cpu')

print(f"모델 로드 완료: {save_directory} elapsed time: {time.time() - start_tick}")

#%%
def generate_text_step_by_step(prompt, max_length=50):
    # 입력 텍스트를 토큰으로 변환
    input_ids = tokenizer.encode(prompt, return_tensors="pt").to(model.device)

    # 초기 설정
    output_ids = input_ids
    model.eval()

    with torch.no_grad():
        for _ in range(max_length):
            # 다음 토큰 예측
            outputs = model(output_ids)
            next_token_logits = outputs.logits[:, -1, :]

            # 다음 토큰 선택
            next_token = torch.argmax(next_token_logits, dim=-1).unsqueeze(-1)

            # 토큰 추가
            output_ids = torch.cat([output_ids, next_token], dim=-1)

            # 생성된 텍스트 출력
            generated_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
            print(generated_text)

            # 문장이 끝났는지 확인
            if next_token.item() == tokenizer.eos_token_id:
                break
#%%
# 예시 사용
prompt = "지구의 위성은 무엇이 있을까요?"
generate_text_step_by_step(prompt, max_length=20)
