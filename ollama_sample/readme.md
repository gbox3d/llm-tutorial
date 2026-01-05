## ollama cli

### setup

https://ollama.com/download

### update

리눅스에서는 별도의 update 명령어가 없으며, 설치 스크립트를 다시 실행하는 방식이 권장됩니다.  
이 과정에서 기존 설정이나 모델 데이터는 보존되고 바이너리만 교체됩니다.  

```bash
curl -fsSL https://ollama.com/install.sh | sh

# 1. 설정 변경 내용 반영 (Warning 해결)
sudo systemctl daemon-reload

# 2. 서비스 재시작 (새 바이너리 실행)
sudo systemctl restart ollama

# 서비스 상태 확인 (Active 시간과 version 확인)
systemctl status ollama

# 커맨드라인에서 버전 확인
ollama --version


```

### 실행하기

```bash
ollama list
ollama run exaone3.5:2.4b
ollama serve # 우분투의 경우는 자동 실행됨
```

### 프로세스로 실행

```bash
pm2 start "ollama serve" --name ollama

```



### proxy

```bash
python ollama_proxy.py
```
