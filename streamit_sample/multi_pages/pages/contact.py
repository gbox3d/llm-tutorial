import streamlit as st
import time
import numpy as np

st.set_page_config(page_title="contact Demo", page_icon="📈")

st.markdown("# Contact Demo")
st.sidebar.header("Contact Demo")
st.write(
    """This demo illustrates a combination of plotting and animation with
Streamlit. We're generating a bunch of random numbers in a loop for around
5 seconds. Enjoy!"""
)