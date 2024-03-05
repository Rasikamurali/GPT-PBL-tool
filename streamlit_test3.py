import streamlit as st
import pandas as pd
import numpy as np

import openai 
import os 
import base64
from fpdf import FPDF
from dotenv import load_dotenv

load_dotenv() 

openai.api_key = os.getenv('OPENAI_API_KEY')

#openai.api_key = os.environ.get('API_KEY')
#gpt_model = "gpt-4"
gpt_model = "gpt-3.5-turbo"

def create_download_link(val, filename):
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'

# Step 1: Define the structure of your Streamlit app
def main():
    st.title("Educational Technology Course Assistant")
    # Step 2: Define variables to hold data
    goals = []
    lesson_goals = ""
    objectives = []
    objective = ""
    tasks = []
    task = ""
    slides = []
    final_output = {}


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
            for goal in goals: 
                user_goals.append(goal)
                #print(user_goals)
            
            #objectives = ["Objective 1", "Objective 2", "Objective 3", "Objective 4", "Objective 5", "Objective 6", "Objective 7", "Objective 8", "Objective 9", "Objective 10", "Objective 11", "Objective 12", "Objective 13", "Objective 14", "Objective 15"]
            

    if not objectives:
        prompt2 = "Please generate 15 learning objectives based on the following learning goals and educational materials."
        # lg = st.text_input("Pick your lesson goals", key ='input_goals')
        # #print(lg)
        # lesson_goals =""
        # indexes = []
        # for i in range(len(list(lg))): 
        #     #print(i)
        #     if i%2 == 0:
        #         # print(type(lg[i]))
        #         index = int(lg[i])
        #         lesson_goals = lesson_goals + goals[index]
        
        
        # print(lesson_goals)

        lg = st.text_input("Pick your lesson goals (Enter the indexes separated by commas)", key='input_goals')
        indexes = [int(index.strip()) for index in lg.split(",") if index.strip().isdigit()]
        lesson_goals = ""
        for index in indexes:
            if 0 <= index < len(user_goals):
                lesson_goals += user_goals[index] + "\n"
    
        prompt2a = prompt2 + " Materials: " + materials + " Goals: " + lesson_goals
        #print(prompt2a)
        if st.button("Generate Objectives", key='create_objectives'):
            response = openai.chat.completions.create(
            model=gpt_model,
            messages=[
                {"role": "system", "content": "You are a research and writing assistant"},
                {"role": "user", "content": prompt2a}]
            )
            objectives = response.choices[0].message.content.split("\n")
            #objectives = ["Objective 1", "Objective 2", "Objective 3", "Objective 4", "Objective 5", "Objective 6", "Objective 7", "Objective 8", "Objective 9", "Objective 10", "Objective 11", "Objective 12", "Objective 13", "Objective 14", "Objective 15"]

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
            #tasks = ["Task 1", "Task 2", "Task 3", "Task 4", "Task 5"]

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
            #slides = ["Slide 1: Introduction", "Slide 2: Objective Explanation", "Slide 3: Task Details", "Slide 4: Learning Resources", "Slide 5: Summary and Conclusion"]

    # Step 4: Display the generated responses
    if goals:
        st.write("Learning Goals:")
        st.write(goals)
        final_output['goals'] = goals

    if objectives:
        st.write("Learning Objectives:")
        st.write("\n".join(objectives))
        final_output['objectives'] = objectives

    if tasks:
        st.write("Learning Tasks:")
        st.write("\n".join(tasks))
        final_output['tasks'] = tasks

    if slides:
        st.write("Slides Outline:")
        st.write("\n".join(slides))
        final_output['slides'] = slides

    export_as_pdf = st.button("Export Report")

    if export_as_pdf:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        for key, value in final_output.items():  # Corrected the iteration
            pdf.cell(40, 10, key)
            pdf.cell(30, 10, value)
            pdf.ln()  # Move to the next line

        pdf_bytes = pdf.output(dest="S").encode("latin-1")

        html = create_download_link(pdf_bytes, "test")

        st.markdown(html, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
    
