#%%
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

import time
import os
from dotenv import load_dotenv
# .env 파일 로드 및 Pinecone 초기화
load_dotenv('../.env')

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

model = AutoModelForCausalLM.from_pretrained(model_name)
model.save_pretrained(model_save_directory)
print(f"모델 저장 완료: {model_save_directory}")
# %%
