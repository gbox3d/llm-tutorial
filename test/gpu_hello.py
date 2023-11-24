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
model_name = config['model_name']

#%%
tokenizer = AutoTokenizer.from_pretrained(model_name,token=auth_token)
#%%
pipeline = transformers.pipeline(
    task="text-generation",
    model=model_name,
    torch_dtype=torch.float16,
    device_map="auto",
    token=auth_token
)
#%%
def gen(x, max_length=200):
    sequences = pipeline(
        x,
        do_sample=True,
        top_k=10,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        max_length=max_length,
    )
    return sequences[0]["generated_text"].replace(x, "")

#%%
print(gen("Hello, how are you?"))
# %%
print(gen('전주시에 대해 알려줘'),500)
# %%
print(gen("대한민국에서 유명한 인공지능 유튜버 3명만 나열해봐.", 500))
# %%
print(gen("페미니즘에 대해 한글로 설명해줘", 500))

# %%
print(gen("""
          전북 전주시 덕진동에 있는 공원이다.전주역 북쪽 3 km 지점에 있는 덕진호 일대의 유원지로, 시민공원이라고도 한다. 
          덕진호의 유래는 서기 901년 후백제를 건국한 견훤이 도서방위를 위해 늪을 만들었다는 설이 있고, 동국여지승람에는 전주가 3면이 산으로 둘러싸인 분지로, 
          북쪽만 열려있는 탓에 땅의 기운이 낮아 가련산과 건지산 사이를 제방으로 막아 저수함으로써 지맥이 흘러내리지 않도록 했다고 전해진다. 
          이상내용을  참고하여 덕진공원에 대해 알려주세요
          """
          ),500)

# %%
