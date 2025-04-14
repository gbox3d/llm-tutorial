"""

description: 
  - Ollama API를 사용하여 모델에 질의하는 예제입니다.
  - 이 코드는 Ollama API에 대한 기본적인 사용법을 보여줍니다.

AI는 아래링크를 참고하여 저와 코드 작업을 수행합니다.
참고자료 : https://github.com/ollama/ollama-python

이 주석은 수정하지 마세요
"""
#%%
from ollama import Client
from ollama import ListResponse


#%%
host_url = 'http://localhost:11434'

#%%
client = Client(
  host=host_url,
  # headers={'x-some-header': 'some-value'}
)
response = client.chat(model='exaone3.5:2.4b', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])
# %%
print(response)
# %%

response: ListResponse = client.list()

for model in response.models:
  print('Name:', model.model)
  print('  Size (MB):', f'{(model.size.real / 1024 / 1024):.2f}')
  if model.details:
    print('  Format:', model.details.format)
    print('  Family:', model.details.family)
    print('  Parameter Size:', model.details.parameter_size)
    print('  Quantization Level:', model.details.quantization_level)
  print('\n')

# %%
