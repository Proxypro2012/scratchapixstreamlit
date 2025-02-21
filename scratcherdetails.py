import streamlit as st
import os

##########################
# Function to Fetch User Info from Scratch API
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





@st.cache_data(ttl=300)  # Cache for 5 minutes to reduce API calls
def get_user_info(username):
    url = f"https://api.scratch.mit.edu/users/{username}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 429:
        st.error("Too many requests. Please wait a moment and try again.")
        return None
    else:
        return f"Error: {response.status_code}"
    
        st.error(f"Error {response.status_code}: Unable to fetch user data.")
        return None

##########################
# Streamlit UI
##########################


USERNAME = os.environ.get("SCRATCH_USERNAME")
PASSWORD = os.environ.get("SCRATCH_PASSWORD")
session = scratch_login(username=str(USERNAME), password=str(PASSWORD))
print("Logged in!")
# Page Layout
st.set_page_config(page_title="Scratch User Info", layout="centered")

r1col1, r1col2, r1col3 = st.columns([1, 2, 1])
r2col1, r2col2, r2col3 = st.columns([1, 2, 1])
r3col1, r3col2, r3col3 = st.columns([1, 2, 1])
r4col1, r4col2, r4col3 = st.columns([1, 2, 1])
r5col1, r5col2, r5col3 = st.columns([1, 2, 1])

# Title & Instructions
with r1col2:
    st.title("Scratch Public User Info")
    st.info("Use the sidebar to fetch a Scratch user's information.")


fetch_username = st.sidebar.text_input("Enter a Scratchers username: ")
if st.sidebar.button("Fetch Info"):
# Sidebar Input
fetch_username = st.sidebar.text_input("Enter a Scratcher's username:")
if st.sidebar.button("Fetch Info") and fetch_username:
    data = get_user_info(fetch_username)
    print(data)

    username = data["username"]
    id = data["id"]
    scratchteam = data["scratchteam"]
    status = data['profile']["status"]
    bio = data['profile']["bio"]


    if scratchteam == True:
        scratchteam = "Yes"
    if data:  # Check if data is valid before accessing keys
        try:
            username = data.get("username", "N/A")
            user_id = data.get("id", "N/A")
            scratchteam = "Yes" if data.get("scratchteam", False) else "No"
            profile = data.get("profile", {})

            status = profile.get("status", "No status available")
            bio = profile.get("bio", "No bio available")

            with r2col2:
                st.write(f"**Scratch Team:** {scratchteam}")
                st.write(f"**Username:** {username}")
                st.write(f"**User ID:** {user_id}")

            with r2col3:
                st.write(f"**Status:** {status}")
                st.write(f"**Bio:** {bio}")

            # Profile Picture
            source_url = f"https://cdn2.scratch.mit.edu/get_image/user/{user_id}_200x200.png?v="
            with r3col2:
                st.header("Profile Picture")
            with r4col2:
                st.image(source_url, width=200)

        except KeyError as e:
            st.error(f"Missing expected data: {e}")
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

    



        st.warning("No data found for this user. Check the username and try again.")
