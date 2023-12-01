#%%
from dotenv import load_dotenv
import os

from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders.csv_loader import CSVLoader

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.retrievers.multi_query import MultiQueryRetriever

# .env 파일 로드
load_dotenv()

#%%
# 임베딩 모델 초기화
openai_embeddings = OpenAIEmbeddings()

# 저장된 벡터 저장소 로드
chroma_store = Chroma(
    persist_directory='./stores/chroma_store',
    embedding_function=openai_embeddings
                      )

#%%
#retriever 생성

llm = ChatOpenAI(
    model_name=os.getenv('OPENAI_MODEL_NAME'),
    temperature=0)

print(llm)

#%%
question = '덕진공원 에 대해서 알려줘'
#%%
retriever_from_llm = MultiQueryRetriever.from_llm(
    llm=llm,
    retriever=chroma_store.as_retriever()
    )
docs = retriever_from_llm.get_relevant_documents(question)
print(docs) 

# %%
qa_chain = RetrievalQA.from_chain_type(llm,retriever=chroma_store.as_retriever())
result = qa_chain({"query": "정읍사에 대해서 알려줘" })
print(result)

# %%
docs = chroma_store.similarity_search(question, k=10)

for doc in docs:
    print(doc)
    

# %%
