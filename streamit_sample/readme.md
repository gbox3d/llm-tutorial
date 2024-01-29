# streamlit my tutorial

```bash

streamlit run any_file.py

```

## Debugging

launch.json 에 아래 내용 추가  
```json
{
    "name": "Python: Streamlit",
    "type": "python",
    "request": "launch",
    "module": "streamlit",
    "args": [
        "run",
        "${file}",
        "--server.port",
        "8501",
        "--",
        "--debugger",
        "--verbose"
    ],
    "console": "integratedTerminal",
    "justMyCode": true,
    "cwd": "${fileDirname}"
}
```

## upload issue

macosx 에서 로컬 파일을 업로드 할 때, 403에러가 발생 하면 config.toml 파일에 아래 내용 추가  

```toml
[server]
enableCORS = false
enableXsrfProtection = false
```