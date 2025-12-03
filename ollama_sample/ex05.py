#!/usr/bin/env python3
"""
Ollama 채팅 스크립트 (개선 버전)
시작할 때 로컬 모델 목록을 보여주고
번호를 선택하면 그 모델로 대화를 시작한다.

추가 기능:
- 대화 중 명령어 지원 (/help, /exit, /save, /params, /summary)
- 대화 내용 파일로 저장
- 모델 매개변수 조절 가능
- 긴 대화 자동 요약 및 메모리 관리
"""
import sys
import json
import argparse
import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

try:
    import ollama
    from ollama import chat
except ImportError:
    print("⚠️  'ollama' 패키지가 설치되어 있지 않습니다.")
    print("pip install ollama 명령으로 설치하세요.")
    sys.exit(1)


def parse_arguments():
    """명령줄 인수 처리"""
    parser = argparse.ArgumentParser(description="Ollama 모델과 대화하는 스크립트")
    parser.add_argument("-m", "--model", help="사용할 모델 이름")
    parser.add_argument("-t", "--temperature", type=float, default=0.7,
                        help="모델 temperature 값 (기본값: 0.7)")
    parser.add_argument("-s", "--save", help="대화 내용을 저장할 파일 경로")
    parser.add_argument("--max-messages", type=int, default=20,
                        help="자동 요약 전 최대 메시지 수 (기본값: 20)")
    parser.add_argument("--no-summary", action="store_true",
                        help="자동 요약 기능 비활성화")
    return parser.parse_args()


def pick_model() -> str:
    """설치된 모델 목록을 보여주고 사용자가 선택하게 함"""
    try:
        # 설치된 모델 목록 가져오기
        models_resp = ollama.list()
        models = models_resp.models

        if not models:
            print("⚠️  로컬에 모델이 없습니다. 먼저 `ollama pull <model>` 로 가져오세요.")
            sys.exit(1)

        # 목록 출력
        print("=== 사용 가능한 모델 ===")
        for i, m in enumerate(models):
            name = m.model
            
            # size 처리 (버전에 따라 다를 수 있음)
            size_str = "알 수 없음"
            if hasattr(m, "size"):
                if hasattr(m.size, "human_readable") and callable(m.size.human_readable):
                    size_str = m.size.human_readable()
                elif isinstance(m.size, (int, float)):
                    size_str = f"{m.size / (1024**3):.1f} GB"
                elif m.size:
                    size_str = str(m.size)
            
            # 수정 시간 처리
            mod_time = "알 수 없음"
            if hasattr(m, "modified_at") and m.modified_at:
                if hasattr(m.modified_at, "strftime"):
                    mod_time = m.modified_at.strftime("%Y-%m-%d %H:%M")
                else:
                    mod_time = str(m.modified_at)
            
            print(f"[{i}] {name:20}  {size_str:>8}  (수정일: {mod_time})")

        # 번호 입력
        while True:
            sel = input("\n번호를 선택하세요 ▶ ")
            try:
                idx = int(sel)
                if 0 <= idx < len(models):
                    return models[idx].model
            except ValueError:
                pass
            print("잘못된 입력입니다. 다시 선택하세요.")
    
    except Exception as e:
        print(f"⚠️  모델 목록을 가져오는 중 오류가 발생했습니다: {e}")
        sys.exit(1)


def format_message(role: str, content: str) -> str:
    """메시지를 포맷팅"""
    if role == "user":
        return f"\033[1;32mYou:\033[0m {content}"
    else:
        return f"\033[1;36mAI:\033[0m {content}"


def save_conversation(messages: List[Dict[str, str]], filepath: Optional[str] = None) -> str:
    """대화 내용을 파일로 저장"""
    if not filepath:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"ollama_chat_{timestamp}.md"
    
    path = Path(filepath)
    
    # 마크다운 형식으로 저장
    with open(path, "w", encoding="utf-8") as f:
        f.write("# Ollama 채팅 기록\n\n")
        f.write(f"날짜: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        for msg in messages:
            role = "🧑 사용자" if msg["role"] == "user" else "🤖 AI"
            f.write(f"## {role}\n\n{msg['content']}\n\n")
    
    return str(path.absolute())


def show_help():
    """도움말 표시"""
    print("\n=== 사용 가능한 명령어 ===")
    print("/help     - 이 도움말 표시")
    print("/exit     - 대화 종료")
    print("/save     - 대화 내용 저장")
    print("/params   - 현재 모델 매개변수 확인/변경")
    print("/summary  - 지금까지의 대화 요약 및 메모리 정리")
    print("/show mem - 현재 메모리에 저장된 대화 내용 표시")
    print("==================\n")


def update_parameters(params: Dict[str, Any]) -> Dict[str, Any]:
    """모델 매개변수 업데이트"""
    print("\n=== 현재 매개변수 ===")
    for key, value in params.items():
        print(f"{key}: {value}")
    
    print("\n변경할 매개변수를 'key=value' 형식으로 입력하세요.")
    print("예: temperature=0.8 top_p=0.9")
    print("그냥 Enter 키를 누르면 변경 없이 돌아갑니다.")
    
    user_input = input("\n입력 ▶ ")
    if not user_input.strip():
        return params
    
    # 입력 파싱
    try:
        for pair in user_input.split():
            if "=" in pair:
                key, value = pair.split("=", 1)
                key = key.strip()
                
                # 값 타입 변환 시도
                try:
                    if value.lower() == "true":
                        value = True
                    elif value.lower() == "false":
                        value = False
                    elif "." in value:
                        value = float(value)
                    else:
                        value = int(value)
                except ValueError:
                    # 변환 실패시 문자열로 유지
                    pass
                
                params[key] = value
                print(f"✅ {key} = {value} 설정됨")
    except Exception as e:
        print(f"⚠️  매개변수 업데이트 중 오류 발생: {e}")
    
    return params


def summarize_conversation(model: str, messages: List[Dict[str, str]], 
                       keep_recent: int = 5) -> List[Dict[str, str]]:
    """대화 내용을 요약하고 메모리를 정리"""
    if not messages:
        print("⚠️ 메모리에 저장된 대화 내용이 없습니다.")
        return
    
    print("\n=== 현재 메모리 내용 (전체 메시지 수: {}) ===".format(len(messages)))
    
    for i, msg in enumerate(messages):
        role = msg["role"]
        
        # 역할에 따라 다른 색상과 표시
        if role == "system":
            role_display = "\033[1;33m시스템\033[0m"  # 노란색
            # 요약 내용은 너무 길면 축약
            content = msg["content"]
            if len(content) > 100:
                content = content[:97] + "..."
        elif role == "user":
            role_display = "\033[1;32m사용자\033[0m"  # 녹색
        elif role == "assistant":
            role_display = "\033[1;36mAI    \033[0m"  # 청록색
        else:
            role_display = "\033[1;37m{}    \033[0m".format(role)  # 기본 회색
        
        # 메시지 내용 (너무 길면 축약)
        content = msg["content"]
        if len(content) > 60 and role != "system":  # 시스템 메시지는 이미 처리됨
            content = content[:57] + "..."
        
        # 메시지 번호와 함께 출력
        print(f"[{i:2d}] {role_display}: {content}")
    
    print("=" * 50)
    if len(messages) <= keep_recent + 1:  # 요약할 만큼 메시지가 없으면 그대로 반환
        return messages

    # 요약할 메시지들 (최근 keep_recent 개는 제외)
    messages_to_summarize = messages[:-keep_recent] if keep_recent > 0 else messages
    
    # 요약 내용 구성
    conversation_text = ""
    for msg in messages_to_summarize:
        role = "사용자" if msg["role"] == "user" else "AI"
        conversation_text += f"{role}: {msg['content']}\n\n"
    
    # 요약 프롬프트 작성
    summary_prompt = f"""다음은 사용자와 AI 사이의 대화입니다. 
이 대화의 핵심 내용을 3-5문장으로 요약해주세요. 
중요한 정보, 결정사항, 질문과 답변을 포함해주세요.

=== 대화 내용 ===
{conversation_text}

=== 요약 ==="""
    
    try:
        print("\n🔄 대화 내용을 요약하는 중...")
        
        # 요약 요청
        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": summary_prompt}],
            options={"temperature": 0.3}  # 요약은 낮은 temperature로
        )
        
        summary = response.message.content
        print(f"✅ 요약 완료: {len(messages_to_summarize)}개 메시지 → 요약")
        
        # 새 메시지 목록 구성: 시스템 메시지 + 최근 메시지들
        new_messages = [
            {"role": "system", "content": f"이전 대화 요약: {summary}"}
        ]
        
        # 최근 메시지 추가
        if keep_recent > 0:
            new_messages.extend(messages[-keep_recent:])
        
        return new_messages
        
    except Exception as e:
        print(f"⚠️ 대화 요약 중 오류 발생: {e}")
        print("⚠️ 요약을 건너뛰고 원래 메시지를 유지합니다.")
        return messages


def main() -> None:
    """메인 함수"""
    args = parse_arguments()
    
    # 모델 선택
    model = args.model if args.model else pick_model()
    
    # 모델 매개변수 초기화
    params = {
        "temperature": args.temperature,
        "top_p": 0.9,
        "top_k": 40,
    }
    
    # 메모리 관리 설정
    max_messages = args.max_messages
    auto_summary = not args.no_summary
    
    print(f"\n✅ '{model}' 모델로 대화를 시작합니다.")
    print(f"✅ 기본 temperature: {params['temperature']}")
    if auto_summary:
        print(f"✅ 자동 요약: 메시지 {max_messages}개 초과시")
    else:
        print("❌ 자동 요약 비활성화됨")
    print("✅ 명령어 도움말은 /help 를 입력하세요.\n")

    messages = []
    try:
        while True:
            try:
                user_input = input("\033[1;32mYou:\033[0m ")
            except (EOFError, KeyboardInterrupt):
                print("\n👋 종료합니다.")
                break
            
            # 빈 입력이면 무시
            if not user_input.strip():
                continue
                
            # 특수 명령어 처리
            if user_input.startswith("/"):
                cmd = user_input.lower().strip()
                
                if cmd == "/exit":
                    print("👋 종료합니다.")
                    break
                elif cmd == "/help":
                    show_help()
                    continue
                elif cmd == "/save":
                    if not messages:
                        print("⚠️ 저장할 대화 내용이 없습니다.")
                        continue
                    
                    save_path = input("저장할 파일 경로 (기본: 자동 생성): ")
                    filepath = save_conversation(messages, save_path if save_path else None)
                    print(f"✅ 대화 내용이 저장되었습니다: {filepath}")
                    continue
                elif cmd == "/params":
                    params = update_parameters(params)
                    continue
                elif cmd == "/summary":
                    if not messages:
                        print("⚠️ 요약할 대화 내용이 없습니다.")
                        continue
                    
                    # 현재 메시지 수 표시
                    print(f"현재 메시지 수: {len(messages)}개")
                    keep_recent = 3  # 기본값
                    
                    try:
                        keep_input = input("유지할 최근 메시지 수 (기본: 3): ")
                        if keep_input.strip():
                            keep_recent = max(0, int(keep_input))
                    except ValueError:
                        print("잘못된 입력, 기본값 3을 사용합니다.")
                    
                    # 요약 실행
                    new_messages = summarize_conversation(model, messages, keep_recent)
                    
                    # 메모리 업데이트
                    if new_messages != messages:
                        messages = new_messages
                        print(f"✅ 메모리가 업데이트되었습니다. 현재 메시지 수: {len(messages)}개")
                        if messages and messages[0]["role"] == "system":
                            print(f"📝 요약: {messages[0]['content']}")
                    continue
                elif cmd == "/show mem" or cmd == "/show_mem":
                    display_memory(messages)
                    continue
            
            # 대화 기록에 사용자 입력 추가
            messages.append({"role": "user", "content": user_input})
            
            try:
                # Ollama에 요청
                response = chat(
                    model=model,
                    messages=messages,
                    options=params
                )
                
                assistant_reply = response.message.content
                print(f"\033[1;36mAI:\033[0m {assistant_reply}")
                
                # 대화 기록에 모델 응답 추가
                messages.append({"role": "assistant", "content": assistant_reply})
                
                # 자동 요약 체크
                if auto_summary and len(messages) > max_messages:
                    print(f"\n🔄 메시지가 {max_messages}개를 초과했습니다. 자동 요약을 진행합니다...")
                    messages = summarize_conversation(model, messages, keep_recent=5)
                
            except Exception as e:
                print(f"⚠️ 모델 응답 중 오류 발생: {e}")
                # 오류 발생 시 마지막 사용자 메시지는 기록에서 제거
                if messages and messages[-1]["role"] == "user":
                    messages.pop()
    
    finally:
        # 종료 시 대화 저장 여부 확인
        if messages and not args.save:
            save_yn = input("\n대화 내용을 저장하시겠습니까? (y/n): ")
            if save_yn.lower() in ["y", "yes", "예"]:
                filepath = save_conversation(messages)
                print(f"✅ 대화 내용이 저장되었습니다: {filepath}")
        # 명령줄 인수로 저장 옵션이 지정된 경우
        elif messages and args.save:
            filepath = save_conversation(messages, args.save)
            print(f"✅ 대화 내용이 저장되었습니다: {filepath}")


if __name__ == "__main__":
    main()