import streamlit as st

# 사용자로부터 입력 받기
prompt = st.chat_input("Say something")

# 텍스트 에디터 추가하여 두 번째 입력 받기
editor_text1 = st.text_area("Add more text with special characters and new lines",key="editor1" 
                            ,value="This is the default text"
                            )

editor_text2 = st.text_area("Add more text with special characters and new lines",key="editor2")

# 두 입력을 결합하여 출력
if prompt :
    
    combined_text = f"""

{prompt} \n {editor_text1} \n {editor_text2}

    """
    
    print(combined_text)
    
    st.text(combined_text)
