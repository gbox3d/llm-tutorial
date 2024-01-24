import streamlit as st


st.title("Streamlit Tutorial: ex05")

# Using "with" notation
with st.sidebar:
    st.title("Sidebar")
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )
    msg = st.text_input(
        label="Enter your message",
        # value="Hello Streamlit!"
        placeholder="input your message here"
    )
    

if add_radio == "Standard (5-15 days)":
    st.write("You chose Standard shipping")
else:
    st.write("You chose Express shipping")
    
if st.button("Submit"):
    st.write("Your message is: ", msg)
    st.write("Your shipping method is: ", add_radio)