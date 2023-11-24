#%%
import os
import time

from langchain.llms import HuggingFaceHub

from dotenv import load_dotenv
# .env 파일 로드 및 Pinecone 초기화
load_dotenv()

#%%
# HuggingFaceHub 모델 로드
llm_hf = HuggingFaceHub(
    repo_id="google/flan-t5-xl",
    model_kwargs={"temperature":0.9 }
)
     
# %%
text = "Why did the chicken cross the road?"

print(llm_hf(text))
# %%
