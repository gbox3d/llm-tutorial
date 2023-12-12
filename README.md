# llm-tutorial

## .env file

```bash
OPENAI_API_KEY=YOUR_API_KEY
OPENAI_MODEL_NAME=YOUR_MODEL_NAME #"gpt-3.5-turbo-1106"
HUGGINGFACEHUB_API_TOKEN=YOUR_API_TOKEN

```

## wget 으로 싸이트 전체 다운로드

```bash

wget -r -A.html -P langchain-docs https://api.python.langchain.com/en/stable/

wget --recursive --no-clobber --page-requisites --html-extension --convert-links --restrict-file-names=windows --domains llm-guide.readthedocs.io --no-parent https://www.wku.ac.kr/

```
