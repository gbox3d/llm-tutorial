#%%
# from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import BaseOutputParser

from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda

import time
import os
from dotenv import load_dotenv
load_dotenv('../../.env')
# chat = ChatOpenAI(temperature=0.8)

import streamlit as st


st.title("LangChain Tutorial Custom OutputParser")

with st.spinner("prepare llm..."):
    # time.sleep(3)
    llm = ChatOpenAI(temperature=0.8)
    st.header("LLM prepared.")
    st.write(f"api key : {os.getenv('OPENAI_API_KEY')}")

#%%
class CommaOutputParser(BaseOutputParser):
    def parse(self, text):
        print("Data passing from llm to parser:", text)
        items = text.strip().split(",")
        return list(map(str.strip, items))
    
#%%

_text = st.text_input(
    label="Enter your message",
    value="a,b,c",
    placeholder="input your message here"
)

chain = RunnableLambda( lambda x : x ) | CommaOutputParser()

if st.button("Submit"):
    st.write("Your message is: ", _text)

    answer = chain.invoke(_text)
    st.text(f"결과 : {answer} , type : {type(answer)}")


# p = CommaOutputParser()
# p.parse("a, b, c")
# %%

