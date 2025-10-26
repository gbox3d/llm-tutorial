#!/usr/bin/env python
# -*- coding: utf-8 -*-
#%%
# import ollama
from ollama import Client, ListResponse


# 클라이언트 초기화 (내부 서버 연결)
client = Client(host='https://ailab.miso.center:22244/')


#%%
    
response: ListResponse = client.list()

for model in response.models:
    print(f"모델명: {model.model}")
    print(f"  수정 날짜: {model.modified_at}")
    print(f"  크기: {model.size / 1024 / 1024:.2f} MB")
    
    # 모델 상세 정보가 있는 경우
    if model.details:
        print(f"  포맷: {model.details.format}")
        print(f"  모델 계열: {model.details.family}")
        print(f"  파라미터 크기: {model.details.parameter_size}")
        print(f"  양자화 레벨: {model.details.quantization_level}")
    print()

#%%
model_name = response.models[0].model
prompt = "'미','라','클' 로 삼행시 지어봐"
answer = client.generate(model=model_name, prompt=prompt)

print(f"응답: {answer['response']}")
