#!/usr/bin/env python3
"""
Ollama 채팅 스크립트
시작할 때 로컬‑모델 목록을 보여주고
번호를 선택하면 그 모델로 대화를 시작한다.
"""
import sys
import ollama
from ollama import chat


def pick_model() -> str:
    # 설치된 모델 목록 가져오기
    models_resp = ollama.list()               # → ListResponse 객체&#8203;:contentReference[oaicite:0]{index=0}
    models = models_resp.models

    if not models:
        print("⚠️  로컬에 모델이 없습니다.  먼저 `ollama pull <model>` 로 가져오세요.")
        sys.exit(1)

    # 목록 출력
    print("=== 사용 가능한 모델 ===")
    for i, m in enumerate(models):
        name = m.model
        size = (m.size.human_readable()       # ByteSize → '4.1 GB' 등
                if getattr(m.size, "human_readable", None)
                else f"{m.size or 'unknown'}")
        mod_time = (m.modified_at.strftime("%Y-%m-%d %H:%M")
                    if m.modified_at else "unknown")
        print(f"[{i}] {name:20}  {size:>8}  (modified {mod_time})")

    # 번호 입력
    while True:
        sel = input("번호를 선택하세요 ▶ ")
        try:
            idx = int(sel)
            if 0 <= idx < len(models):
                return models[idx].model
        except ValueError:
            pass
        print("잘못된 입력입니다. 다시 선택하세요.")


def main() -> None:
    model = pick_model()
    print(f"\n✅ '{model}' 모델로 대화를 시작합니다.\n")

    messages = []
    while True:
        try:
            user_input = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print("\n👋 종료합니다.")
            break

        # Ollama 에 요청
        response = chat(
            model=model,
            messages=messages + [{'role': 'user', 'content': user_input}],
        )

        assistant_reply = response.message.content
        print(f"{model}: {assistant_reply}\n")

        # 히스토리 갱신
        messages += [
            {'role': 'user', 'content': user_input},
            {'role': 'assistant', 'content': assistant_reply},
        ]


if __name__ == "__main__":
    main()
