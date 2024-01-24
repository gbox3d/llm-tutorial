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
    "justMyCode": true
}
```
        