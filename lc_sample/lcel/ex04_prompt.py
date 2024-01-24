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
st.title("LangChain Tutorial ")

with st.spinner("prepare llm..."):
    llm = ChatOpenAI(temperature=0.8)
    time.sleep(0.5)
    st.header("LLM prepared.")
    st.write(f"api key : {os.getenv('OPENAI_API_KEY')}")
    

def log_chain(x):
    print("log : ", x) # 이전 단계에서 넘어온 데이터를 확인할 수 있다.
    return x

rbLogChain = RunnableLambda(log_chain)

#%% 단문/문장 구분하기
prompt = ChatPromptTemplate.from_template(
    """
    {instruction}
    \n\n
    ================================
    \n\n
    
    내용 : {question}
    """
)

chain = prompt | log_chain | llm | StrOutputParser()

intruction_text = st.text_area(
    label="Instruction",
    value="""
다음에 오는 내용이 단어가 2단어 이하이면 "단문"으로, 3단어 이상이면 "문장"으로 답해주세요.
"단어" 라는 기준의 의미는 띄어쓰기로 구분되는 단어입니다.
    """,
    height=200
)

msg = st.text_input(
    label="Enter your message",
    placeholder="input your message here"
)

if st.button("Submit") :
    
    if msg == "" :
        st.warning("메시지를 입력해주세요.")
        st.stop()
    if intruction_text == "" :
        st.warning("Instruction을 입력해주세요.")
        st.stop()

    with st.spinner("wait for answer..."):
        answer = ""
        answer = chain.invoke({
            "instruction": intruction_text,
            "question": msg
        })
        
        st.write(f"답변 : {answer}")
    
    









