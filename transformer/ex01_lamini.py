#%%
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import pipeline
import torch

import time
import os


import json
import textwrap

checkpoint = "MBZUAI/LaMini-Flan-T5-783M" 
# checkpoint = "MBZUAI/LaMini-Neo-1.3B" 
# checkpoint = "MBZUAI/LaMini-GPT-1.5B" 



tokenizer = AutoTokenizer.from_pretrained(checkpoint)
base_model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint,
                                             device_map='auto',
                                             torch_dtype=torch.float16,
                                             load_in_8bit=True)

pipe = pipeline('text2text-generation', 
                 model = base_model,
                 tokenizer = tokenizer,
                 max_length=512, 
                 do_sample=True,
                 temperature=0.01,
                 top_p=0.95,
                 repetition_penalty=1.15
                 )
#%%
def get_prompt(instruction):
    prompt_template = f"Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:\n{instruction}\n\n### Response:"
    return prompt_template

def parse_text(data):
    for item in data:
        text = item['generated_text']
        wrapped_text = textwrap.fill(text, width=100)
        print(wrapped_text +'\n\n')

# print(get_prompt('What is the meaning of life?'))
# %%time
start_time = time.time()
gen_txt = pipe(
    get_prompt("What are the differences between alpacas, vicunas and llamas?"), 
    #  max_new_tokens=64,
     num_return_sequences=1
     )

parse_text(gen_txt)

print(f"Time taken: {time.time() - start_time:.2f} seconds")


# %%
