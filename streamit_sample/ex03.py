import streamlit as st

agree = st.checkbox('I agree')
if agree:
    st.write('Great!')
else:
    st.write('Not great!')
    
check1 = st.checkbox("Check me out")
check2 = st.checkbox("Check me out too")

onof = st.toggle("Toggle me")

if onof :
    st.write("Toggle on")
else :
    st.write("Toggle off")
    
_radio = st.radio("Radio",("The Office","Parks and Recreation","Community"))
    
age = st.slider('How old are you?', 0, 130, 25)
st.write("I'm ", age, 'years old')
    
if st.button("Hello") : 
    st.write("Why hello there")
    st.write(f"checkbox value : {agree} , {check1} , {check2}")
    st.write(f"toggle value : {onof}")
    st.write(f"radio value : {_radio}")
else :
    st.write("Goodbye")
