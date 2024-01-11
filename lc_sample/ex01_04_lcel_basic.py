#%%
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import BaseOutputParser
from langchain.schema.output_parser import StrOutputParser

import time
import os
from dotenv import load_dotenv
load_dotenv('../.env')

llm = ChatOpenAI(temperature=0.8)

#%% 단문/문장 구분하기
prompt = ChatPromptTemplate.from_template(
    """
    다음에 오는 내용이 단어 하나이면 "단문"으로, 두 단어 이상이면 "문장"으로 답해주세요.
    \n\n
    ================================
    \n\n
    
    내용 : {question}
    """
)

chain = prompt | llm | StrOutputParser()

chain.invoke({
    "question": "한국 의 수도 는 어디 입니까?"
})


# %%
