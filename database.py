import streamlit as st
from google.cloud import firestore

# Authenticate to Firestore with the JSON account key.
db = firestore.Client.from_service_account_json("firestore-key.json")

# Streamlit widgets to let a user create a new post
title = st.text_input("Username")
l_goals = st.text_input("Learning Goals")
l_obj = st.text_input("Learning Objectives")
l_tasks = st.text_input("Learning Tasks")
l_slides = st.text_input("Learning Slides")

submit = st.button("Submit new interaction")

if submit:
    if title and l_goals and l_obj and l_tasks and l_slides:
        doc_ref = db.collection("Interactions").document(title)
        doc_ref.set({
            "learning_goals": l_goals,
            "learning_obj": l_obj,
            "learning_tasks": l_tasks,
            "learning_slides": l_slides
        })
        st.success("Interaction submitted successfully!")
    else:
        st.error("Please fill in all fields before submitting.")

# Render existing posts
posts_ref = db.collection("Interactions")
for doc in posts_ref.stream():
    post = doc.to_dict()
    l_goals = post['learning_goals']
    l_obj = post['learning_obj']
    l_tasks = post['learning_tasks']

    st.subheader(f"Post: {l_goals}")
    st.subheader(f"Post: {l_obj}")
    st.subheader(f"Post: {l_tasks}")
