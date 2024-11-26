#%%
import json

import requests

from dotenv import load_dotenv
load_dotenv()

#%%
url = "http://localhost:8000/stream"
# message = "Hello, how are you?"

# headers = {"Content-type": "application/json"}
# data = {"message": "Hello, how are you?"}

# with requests.post(url, data=json.dumps(data), headers=headers, stream=True) as r:
#     for chunk in r.iter_content(1024):
        # print(chunk)
# %%

while True:
    message = input(">> ")
    headers = {"Content-type": "application/json"}
    data = {"message": message}
    with requests.post(url, data=json.dumps(data), headers=headers, stream=True) as r:
        for chunk in r.iter_content(1024):
            print(chunk.decode('utf-8'), end="",flush=True)
        print("\n done")

# %%
