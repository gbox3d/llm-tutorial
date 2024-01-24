import streamlit as st

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False
    st.session_state.placeholder = "Enter some text here"

text_input = st.text_input(
    "Enter some text 👇",
    label_visibility=st.session_state.visibility,
    disabled=st.session_state.disabled,
    placeholder=st.session_state.placeholder,
)

if text_input:
    st.write("You entered: ", text_input)
    print(text_input)
    
txt = st.text_area(
    label="Text to analyze",
    value = "It was the best of times, it was the worst of times, it was the age of "
    "wisdom, it was the age of foolishness, it was the epoch of belief, it "
    "was the epoch of incredulity, it was the season of Light, it was the "
    "season of Darkness, it was the spring of hope, it was the winter of "
    "despair, (...)",
    placeholder="Type something"
    )

if st.button("Analyze"):
    st.write("Analyzing the text...")
    st.write(f'You wrote {len(txt)} characters.')