import streamlit as st
import pandas as pd
import numpy as np

import openai 
import os 
import base64
from fpdf import FPDF


st.title('Welcome to the Learning Center')

#gpt_model = "gpt-4"
gpt_model = "gpt-3.5-turbo"

materials = st.text_input("Please out in your target object/ materials")


prompt1 = "please generate 10 learning goals that a teacher could base a lesson on using the following educational materials and processes: " + materials
response = openai.chat.completions.create(
  model=gpt_model,
  messages=[
      {"role": "system", "content": "You are a research and writing assistant for an educational technology course"},
      {"role": "user", "content": prompt1 }
      ]
)
goals = response.choices[0].message.content.split("\n")

for line in goals:
    st.write(str(line))

user_goals = st.text_input("Please go through the goals and pick any 3 of them. Keep in mind that the goals start from 0 - 9")

lesson_goals = ""
print(list(user_goals))
for i in range(len(list(user_goals))): 
    if i%2 == 0: 
        print(user_goals[i])
        lesson_goals = lesson_goals + goals[int(i)]

st.write(lesson_goals)


prompt2 = "Please generate 15 learning objectives based on the following learning goals and educational materials."
prompt2a = prompt2 + "Materials: " + materials + " Goals: " + lesson_goals

### Generate and print out

response = openai.chat.completions.create(
  model=gpt_model,
  messages=[
      {"role": "system", "content": "You are a research and writing assistant"},
      {"role": "user", "content": prompt2a}]
)
objectives = response.choices[0].message.content.split("\n")

st.subheader("Please note the goals and lesson plans here ")
for line in objectives:
    st.write(str(line))

obj = st.text_input("Please pick a number from 0-14 that represents the objective you are interested in")
print(type(obj))
user_objective = ""
user_objective = user_objective + objectives[int(obj)]

st.write(user_objective)


prompt3 = "Please generate five specific learning tasks for students based on the following objectives, goals, and initial list of materials."
prompt3a = prompt3 + "Materials: " + materials + " Goals: " + lesson_goals + " Objective: " + user_objective
### Generate and print out

st.subheader("Tasks are displayed below")

response = openai.chat.completions.create(
  model=gpt_model,
  messages=[
      {"role": "system", "content": "You are a research and writing assistant for an educational technology course"},
      {"role": "user", "content": prompt3a}]
)
tasks = response.choices[0].message.content.split("\n")

for line in tasks:
    st.write(str(line))


def create_download_link(val, filename):
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'

report_text = "Hello"
export_as_pdf = st.button("Export Report")

if export_as_pdf:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, report_text)
    
    html = create_download_link(pdf.output(dest="S").encode("latin-1"), "test")

    st.markdown(html, unsafe_allow_html=True)
