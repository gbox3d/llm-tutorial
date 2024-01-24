#%%
# from langchain.chat_models import ChatOpenAI
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

st.title("LangChain Tutorial ")

llm = ChatOpenAI(temperature=0.8)

#%% 단문/문장 구분하기
prompt = ChatPromptTemplate.from_template(
    """
    다음에 오는 내용이 단어가 2단어 이하이면 "단문"으로, 3단어 이상이면 "문장"으로 답해주세요.\n
    "단어" 라는 기준의 의미는 띄어쓰기로 구분되는 단어입니다.\n
    \n\n
    ================================
    \n\n
    
    내용 : {question}
    """
)

def log_chain(x):
    print("log : ", x) # 이전 단계에서 넘어온 데이터를 확인할 수 있다.
    return x

rbLogChain = RunnableLambda(log_chain)


chain = prompt | rbLogChain | llm | rbLogChain | StrOutputParser()

_question = st.text_input(
    label="Enter your message",
    # value="Hello Streamlit!"
    placeholder="input your message here"
)

if st.button("Submit"):
    st.write("Your message is: ", _question)

    answer = chain.invoke({
        "question": _question
    })
    
    st.text(f"답변 : {answer}")


# %%
