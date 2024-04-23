import streamlit as st
import pandas as pd
import numpy as np
import secrets
import openai 
import os 
import base64
from fpdf import FPDF
from dotenv import load_dotenv
from google.cloud import firestore
import json
import streamlit as st
from google.oauth2 import service_account
from dotenv import load_dotenv
import os

load_dotenv() 

#openai.api_key = os.getenv('OPENAI_API_KEY')

#openai.api_key = os.environ.get('API_KEY')
api_key = st.secrets["OPENAI_API_KEY"]

openai.api_key = api_key
#gpt_model = "gpt-4"
gpt_model = "gpt-3.5-turbo"

# Authenticate to Firestore with the JSON account key.
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="pblgpt-6bfb0")

def main():
    st.title("Educational Technology Course Assistant")
    title = st.text_input("username")
    # Step 2: Define variables to hold data
    goals = []
    lesson_goals = ""
    objectives = []
    objective = ""
    tasks = []
    task = ""
    slides = []
    doc_data={}
    # Initialize final_output dictionary
    doc_ref = db.collection("Interactions").document(title)

    # Step 3: Create input fields and buttons
    user_goals = []
    if not goals:
        materials = st.text_input("Enter educational materials:")
        prompt1 = "please generate 10 learning goals that a teacher could base a lesson on using the following educational materials and processes: " + materials
        if st.button("Generate Goals", key='generate_goals'):
            response = openai.chat.completions.create(
            model=gpt_model,
            messages=[
                {"role": "system", "content": "You are a research and writing assistant for an educational technology course"},
                {"role": "user", "content": prompt1 }
                ]
            )
            goals = response.choices[0].message.content.split("\n")
            #doc_ref.set({"learning_goals": goals})
            doc_data = {"learning_goals": goals}

    if not objectives:
        prompt2 = "Please generate 15 learning objectives based on the following learning goals and educational materials."
        lg = st.text_input("Pick your lesson goals (Enter the indexes separated by commas)", key='input_goals')
        indexes = [int(index.strip()) for index in lg.split(",") if index.strip().isdigit()]
        lesson_goals = ""
        for index in indexes:
            if 0 <= index < len(user_goals):
                lesson_goals += user_goals[index] + "\n"
    
        prompt2a = prompt2 + " Materials: " + materials + " Goals: " + lesson_goals
        if st.button("Generate Objectives", key='create_objectives'):
            response = openai.chat.completions.create(
            model=gpt_model,
            messages=[
                {"role": "system", "content": "You are a research and writing assistant"},
                {"role": "user", "content": prompt2a}]
            )
            objectives = response.choices[0].message.content.split("\n")
            #doc_ref.set({"learning_objectives": objectives})
            doc_data = {"learning_obj": objectives}

    if not tasks:
        obj = st.text_input("Pick one objective you would like to work on", key='input_obj')
        obj_indexes = [int(idx.strip()) for idx in obj.split(",") if idx.strip().isdigit()]
        user_objectives = ""
        for idx in obj_indexes:
            if 0 <= idx < len(objectives):
                user_objectives += objectives[index] + "\n"
        prompt3 = "Please generate five specific learning tasks for students based on the following objectives, goals, and initial list of materials."
        prompt3a = prompt3 + " Materials: " + materials + " Goals: " + lesson_goals + " Objective: " + objective
        if st.button("Generate Tasks", key='create_tasks'):
            # Placeholder API call to generate tasks
            response = openai.chat.completions.create(
            model=gpt_model,
            messages=[
                {"role": "system", "content": "You are a research and writing assistant for an educational technology course"},
                {"role": "user", "content": prompt3a}]
            )
            tasks = response.choices[0].message.content.split("\n")
            #doc_ref.set({"learning_tasks": tasks})
            doc_data = {"learning_tasks": tasks}

    if not slides:
        tsk = st.text_input("Pick one task you would like to work on", key='input_tsk')
        tsk_indexes = [int(tidx.strip()) for tidx in obj.split(",") if tidx.strip().isdigit()]
        user_tasks = ""
        for tidx in tsk_indexes:
            if 0 <= tidx < len(tasks):
                user_tasks += tasks[tidx] + "\n"
        prompt4 = "Please generate an outline for the slides that a teacher should produce for students to achieve the following task based on the goals, objectives, and initial list of materials."
        prompt4a = prompt4 + " Materials: " + materials + " Goals: " + lesson_goals + " Objective: " + objective + " Task: " + task
        if st.button("Generate Slides Outline", key='create_slides'):
            # Placeholder API call to generate slides outline
            response = openai.chat.completions.create(
            model=gpt_model,
            messages=[
                {"role": "system", "content": "You are a research and writing assistant for an educational technology course"},
                {"role": "user", "content": prompt3a}]
            )
            slides = response.choices[0].message.content.split("\n")
            #doc_ref.set({"learning_slides": slides})
            doc_data = {"learning_slides": slides}

    if doc_data: 
        print(doc_data)
        doc_ref.update(doc_data)
    # Step 4: Display the generated responses
    if goals:
        st.write("Learning Goals:")
        st.write(goals)

    if objectives:
        st.write("Learning Objectives:")
        st.write("\n".join(objectives))
        
    if tasks:
        st.write("Learning Tasks:")
        st.write("\n".join(tasks))
        
    if slides:
        st.write("Slides Outline:")
        st.write("\n".join(slides))

if __name__ == "__main__":
    main()
