import streamlit as st

if 'counter' not in st.session_state:
    st.session_state.counter = 0

st.title("Session Example")

if st.button("Increment"):
    st.session_state.counter += 1

st.markdown(f"## Counter: {st.session_state.counter}")
