#%%
from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers
import torch

import yaml

#%%
#load config.yaml
with open('config.yaml', 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    print(config)
auth_token = config['auth_token']

#%%
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf",token=auth_token)
#%%
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-chat-hf",
    token="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")

#%%
# 사용자의 입력
user_input = "Hello, how are you?"

# 토크나이즈
input_ids = tokenizer.encode(user_input, return_tensors='pt')

# 모델을 통해 예측
output = model.generate(input_ids)

# 예측 결과를 텍스트로 변환
response = tokenizer.decode(output[0], skip_special_tokens=True)

print(response)

# %%

input_ids = tokenizer.encode("대한민국 전주시에 대해 알려줘", return_tensors='pt')
print(input_ids)

# %%
# 모델을 통해 예측
output = model.generate(input_ids)
print(output)
# %%
