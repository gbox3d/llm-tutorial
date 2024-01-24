#%%
from langchain_openai import ChatOpenAI

from langchain.prompts import ChatPromptTemplate
from langchain.schema import BaseOutputParser
from langchain.schema.output_parser import StrOutputParser

from langchain_core.runnables import RunnableLambda

import streamlit as st

import time
import os
from dotenv import load_dotenv
load_dotenv('../../.env')

#%%
st.title("LangChain Tutorial RunnableLambda")

with st.spinner("prepare llm..."):
    # time.sleep(3)
    llm = ChatOpenAI(temperature=0.8)
    st.header("LLM prepared.")
    st.write(f"api key : {os.getenv('OPENAI_API_KEY')}")

def add_five(x):
    return x + 5.0

def multiply_by_two(x):
    return x * 2.0

add_five = RunnableLambda(add_five)
multiply_by_two = RunnableLambda(multiply_by_two)

chain = add_five | multiply_by_two

_number = st.number_input(
    label="Enter your number",
    # value="Hello Streamlit!"
    placeholder="input your number here"
)

if st.button("Submit"):
    st.write("Your number is: ", _number)

    answer = chain.invoke(_number)
    st.text(f"답변 : {answer}")

#%%
def print_step(x):
    print("Data passing from prompt to llm:", x) # 이전 단계에서 넘어온 데이터를 확인할 수 있다.
    return f"[{x}]" # 다음 단계로 넘어가는 데이터를 변경할 수 있다.


rb_print_step = RunnableLambda(print_step)

chain = rb_print_step | rb_print_step | rb_print_step

_question = st.text_input(
    label="Enter your message",
    placeholder="input your message here"
)

if st.button("Submit", key="submit2"):
    st.write("Your message is: ", _question)

    answer = chain.invoke(_question)
    
    st.text(f"결과 : {answer}")
    
    

    


