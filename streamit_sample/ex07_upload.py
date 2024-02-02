import os
import streamlit as st

base_path = './.cache/files/'

st.title("Upload Example")

# 파일리스트 보여주기 항목은 체크박스 있고 삭제 버튼 있음

# 폴더가 없으면 생성
if not os.path.exists(base_path):
    os.makedirs(base_path)

if 'check_list' not in st.session_state:
    st.session_state.check_list = []
if 'files' not in st.session_state:
    st.session_state.files = []

check_list = st.session_state.check_list

#파일저장 
if st.button("save file") : 
    for uploaded_file in st.session_state.files:
        file_content = uploaded_file.read()
        file_path = os.path.join(base_path, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(file_content)
            
    if st.button("Delete"):
        for i in range(len(check_list) - 1, -1, -1):
            check = check_list[i]
            print(check)
            # delete check
            if check[0]:
                os.remove(os.path.join(base_path, check[1]))
                del check_list[i]
                # st.write(f"Delete {check[1]}")
        files = os.listdir(base_path)
        for file in files:
            check_list.append( (st.checkbox(f"{file}"), file))
    else :
        st.session_state.check_list = []
        files = os.listdir(base_path)
        for file in files:
            st.session_state.check_list.append( (st.checkbox(f"{file}"), file))
    
    
else :
    #업로드 할 파일 준비 
    uploaded_files = st.file_uploader("Choose a CSV file to upload", accept_multiple_files=True)

    if uploaded_files is not None:
        st.session_state.files = uploaded_files
                
        if st.button("Delete"):
            for i in range(len(check_list) - 1, -1, -1):
                check = check_list[i]
                print(check)
                # delete check
                if check[0]:
                    os.remove(os.path.join(base_path, check[1]))
                    del check_list[i]
                    # st.write(f"Delete {check[1]}")
                    
            st.session_state.check_list = []
            files = os.listdir(base_path)
            for file in files:
                st.session_state.check_list.append( (st.checkbox(f"{file}"), file))
        else :
            st.session_state.check_list = []
            files = os.listdir(base_path)
            for file in files:
                st.session_state.check_list.append( (st.checkbox(f"{file}"), file))

    
    
    