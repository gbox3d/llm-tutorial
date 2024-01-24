import streamlit as st

col1, col2 = st.columns(2)

with col1:
   st.header("Image")
   st.image("https://static.streamlit.io/examples/cat.jpg")

with col2:
   st.header("UI Widgets")
   st.title("This is a title")
   
   msg = st.text_input(
         label="Enter your message",
         # value="Hello Streamlit!"
         placeholder="input your message here"
    )
   
   if st.button("Submit"):
       st.write("Your message is: ", msg)
   
   

