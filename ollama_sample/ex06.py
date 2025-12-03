#%%
import ollama
from pathlib import Path

# 수업 표준 모델: gemma3 (기본 4b 사이즈 사용 - 가볍고 이미지 인식 가능)
# 학생들 PC 사양이 좋다면 'gemma3:12b'로 변경 가능
MODEL_NAME = "gemma3:12b" 

def analyze_image_with_gemma(image_path):
    p = Path(image_path)
    if not p.exists():
        print("이미지 파일이 없습니다.")
        return

    print(f"Analyzing {p.name} with Google {MODEL_NAME}...")

    # 스트리밍 방식으로 답변 받기
    stream = ollama.chat(
        model=MODEL_NAME,
        messages=[{
            'role': 'user',
            'content': "이 이미지를 설명해줘. 작가와 작품명 만 알려줘.",
            'images': [image_path] # gemma3는 이미지를 바로 이해합니다!
        }],
        stream=True
    )

    print("\n[Gemma3 Response]: ", end='', flush=True)
    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)
    print("\n")
    
print("=== ready ollama ===")

#%%
if __name__ == "__main__":
    # 같은 폴더에 있는 이미지 파일명
    analyze_image_with_gemma("./kiss.jpg")
# %%
