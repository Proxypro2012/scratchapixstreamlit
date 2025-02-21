import requests
import numpy as np
import streamlit as st
import os

##########################


def scratch_login(username, password):
    session = requests.Session()


    # Get CSRF token
    csrf_url = "https://scratch.mit.edu/csrf_token/"
    session.get(csrf_url)
    csrf_token = session.cookies.get("scratchcsrftoken")

    headers = {
        "x-csrftoken": csrf_token,
        "x-requested-with": "XMLHttpRequest",
        "referer": "https://scratch.mit.edu/",
        "user-agent": "Mozilla/5.0"
    }

    login_url = "https://scratch.mit.edu/login/"
    payload = {
        "username": username,
        "password": password
    }

    response = session.post(login_url, json=payload, headers=headers)

    if response.status_code == 200:
        print("Logged in successfully!")
        return session
    else:
        print(f"Login failed. {response.status_code}")
        print(response.text)
        return None





def get_project_info(project_id):
    url = f"https://api.scratch.mit.edu/projects/{project_id}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}"





def get_user_info(username):
    url = f"https://api.scratch.mit.edu/users/{username}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}"
    

##########################


USERNAME = os.environ.get("SCRATCH_USERNAME")
PASSWORD = os.environ.get("SCRATCH_PASSWORD")
session = scratch_login(username=str(USERNAME), password=str(PASSWORD))
print("Logged in!")

r1col1, r1col2, r1col3 = st.columns([1, 2, 1])
r2col1, r2col2, r2col3 = st.columns([1, 2, 1])
r3col1, r3col2, r3col3 = st.columns([1, 2, 1])
r4col1, r4col2, r4col3 = st.columns([1, 2, 1])
r5col1, r5col2, r5col3 = st.columns([1, 2, 1])

with r1col2:
    st.title("Scratch Public User Info")
    st.info("Use the sidebar to fetch a Scratch user's information.")


fetch_username = st.sidebar.text_input("Enter a Scratchers username: ")
if st.sidebar.button("Fetch Info"):
    data = get_user_info(fetch_username)
    print(data)

    username = data["username"]
    id = data["id"]
    scratchteam = data["scratchteam"]
    status = data['profile']["status"]
    bio = data['profile']["bio"]


    if scratchteam == True:
        scratchteam = "Yes"
    else:
        scratchteam = "No"




    with r2col2:
        st.write(f"Scratch Team: {scratchteam}")
        st.write(f"Username: {username}")
        st.write(f"ID: {id}")

    with r2col3:
        st.write(f"Status: {status}")
        st.write(f"Bio: {bio}")


    source_url = f"https://cdn2.scratch.mit.edu/get_image/user/{id}_200x200.png?v="

    with r3col2:
        st.header("Profile Picture")
    with r4col2:
        st.image(source_url, width=200)

    



