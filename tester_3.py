from openai import OpenAI
import streamlit as st
import pandas as pd
import numpy as np
import openai 
import os 
import base64
from fpdf import FPDF
from gpt4 import call_gpt4

# openai.api_key = "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"
st.title('Welcome to the Learning Center')

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    print(message)
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Welcome to learning center. Please put in your materials here"):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        prompt1 ="please generate 10 learning goals that a teacher could base a lesson on using the following educational materials and processes: " + prompt
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})