from google.cloud import bigquery
import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

client = bigquery.Client(project="juan-gomez-fiu")
ACCESS_KEY = os.environ.get("ACCESS_KEY")

if 'user_list' not in st.session_state:
    st.session_state.user_list = []

if 'current_user' not in st.session_state:
    st.session_state.current_user = ""

if 'current_user_workouts' not in st.session_state:
    st.session_state.current_user_workouts = []

def get_users():
       
    query = "SELECT UserId from `juan-gomez-fiu`.SWEpers.Users"

    query_job = client.query(query)
    results = query_job.result() 

    user_ids = [row.UserId for row in results]
    return user_ids

def get_user_workouts(user_id):

    query = f"""SELECT 
        * FROM 
        `juan-gomez-fiu`.SWEpers.Workouts
    WHERE 
        UserId = '{user_id}'
    ORDER BY 
        EndTimestamp DESC
    LIMIT 3"""

    results = client.query(query).result()

    data = [dict(row) for row in results]
    return data



def get_exercise_image(post_text):
    url = "https://api.unsplash.com/search/photos"
    
    headers = {
        "Authorization": f"Client-ID {ACCESS_KEY}"
    }
    
    params = {
        "query": "{post_text} exercise gym",
        "per_page": 1
    }
    
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    if data.get("results"):
        return data["results"][0]["urls"]["regular"]
    
    return None

def add_post(author_id, content, image_url):
    #Line written by GEMINI
    query = f"""
    INSERT INTO `juan-gomez-fiu`.SWEpers.Posts 
    (PostId, AuthorId, Timestamp, ImageUrl, Content)
    
    SELECT 
      CONCAT(
        'post', 
        CAST(IFNULL(MAX(CAST(SUBSTR(PostId, 5) AS INT64)), 0) + 1 AS STRING)
      ),
      '{author_id}',
      CURRENT_DATETIME(),
      '{image_url}',
      '{content}'
      
    FROM `juan-gomez-fiu`.SWEpers.Posts
    """
    
    client.query(query).result()


st.header("Activity Page")
if not st.session_state.user_list:
    st.session_state.user_list = get_users()

current_user = st.selectbox("Select User",["Select a User"] + st.session_state.user_list)
if current_user != "Select a User" and current_user != st.session_state.current_user:
    st.session_state.current_user = current_user
    st.session_state.current_user_workouts = []

st.divider()
if st.session_state.current_user:

    # ONLY fetch data conditionally
    if not st.session_state.current_user_workouts:
        st.session_state.current_user_workouts = get_user_workouts(
            st.session_state.current_user
        )

  
    st.subheader("Workout History")

    for workout in st.session_state.current_user_workouts:
        if st.button(workout["WorkoutId"], key=workout["WorkoutId"]):
            st.session_state.current_workout = workout

    # Show selected workout
    if st.session_state.get("current_workout"):

        
        start_str = st.session_state.current_workout['StartTimestamp'].strftime("%b %d, %H:%M")
        end_str = st.session_state.current_workout['EndTimestamp'].strftime("%H:%M")
        
        #Line written by GEMINI
        details = f"""
        🆔 Workout ID: {st.session_state.current_workout['WorkoutId']}
        📅 Time: {start_str} to {end_str}
        ━━━━━━━━━━━━━━━━━━━━━━━━━━
        📏 Distance: {st.session_state.current_workout['TotalDistance']} miles
        👣 Steps: {st.session_state.current_workout['TotalSteps']}
        🔥 Calories: {st.session_state.current_workout['CaloriesBurned']} kcal
        📍 Start: ({st.session_state.current_workout['StartLocationLat']}, {st.session_state.current_workout['StartLocationLong']})
        """

        # Then display it
        st.text_area("Workout Details", value=details, height=200)
      
    # st.text_area("User Workouts",f"{"\n".join([row["WorkoutId"] for row in st.session_state.current_user_workouts])}")

else:
    st.error("Select a User To View Workouts")


st.divider()
if "show_post_form" not in st.session_state:
    st.session_state.show_post_form = False

# 2. Clicking this button toggles the state permanently
make_post = st.button("Make a Post")
if make_post:
    st.session_state.show_post_form = True


if st.session_state.show_post_form:
    if not st.session_state.current_user:
        st.error("Select a User To Make a Post")
    else:
        post_text = st.text_input("Enter Your Post Content")
        submit_button = st.button("Submit Post")

        if submit_button:
            if post_text: 
                image_url = get_exercise_image(post_text)
                print(image_url)
                add_post(st.session_state.current_user, post_text, image_url)            
                st.session_state.show_post_form = False
                st.rerun() 
            else:
                st.warning("Post content cannot be empty.")