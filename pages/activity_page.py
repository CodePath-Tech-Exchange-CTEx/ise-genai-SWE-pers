import streamlit as st
import os
from dotenv import load_dotenv
from google.cloud import bigquery
from data_fetcher import get_users, get_user_workouts, get_exercise_image, _get_client

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

ACCESS_KEY = os.environ.get("ACCESS_KEY")

if 'user_list' not in st.session_state:
    st.session_state.user_list = []

if 'current_user' not in st.session_state:
    st.session_state.current_user = ""

if 'current_user_workouts' not in st.session_state:
    st.session_state.current_user_workouts = []


def add_post(author_id, content, image_url):
    """Inserts a new post into BigQuery. Lines written by CHATGPT."""
    query = """
    INSERT INTO `juan-gomez-fiu`.SWEpers.Posts 
    (PostId, AuthorId, Timestamp, ImageUrl, Content)
    SELECT 
      CONCAT(
        'post', 
        CAST(IFNULL(MAX(CAST(SUBSTR(PostId, 5) AS INT64)), 0) + 1 AS STRING)
      ),
      @author_id,
      CURRENT_DATETIME(),
      @image_url,
      @content
    FROM `juan-gomez-fiu`.SWEpers.Posts
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("author_id", "STRING", author_id),
            bigquery.ScalarQueryParameter("image_url", "STRING", image_url or ""),
            bigquery.ScalarQueryParameter("content", "STRING", content),
        ]
    )
    try:
        _get_client().query(query, job_config=job_config).result()
    except Exception as e:
        print("BIGQUERY ERROR:", e)
        raise e


st.header("Activity Page")

if not st.session_state.user_list:
    st.session_state.user_list = get_users()

current_user = st.selectbox("Select User", ["Select a User"] + st.session_state.user_list)
if current_user != "Select a User" and current_user != st.session_state.current_user:
    st.session_state.current_user = current_user
    st.session_state.current_user_workouts = []

st.divider()

if st.session_state.current_user:
    if not st.session_state.current_user_workouts:
        st.session_state.current_user_workouts = get_user_workouts(st.session_state.current_user)[:3]

    st.subheader("Workout History")

    for workout in st.session_state.current_user_workouts:
        if st.button(workout["workout_id"], key=workout["workout_id"]):
            st.session_state.current_workout = workout

    if st.session_state.get("current_workout"):
        start_str = st.session_state.current_workout['start_timestamp'][:16]
        end_str = st.session_state.current_workout['end_timestamp'][11:16]

        # Lines written by GEMINI
        details = f"""
        🆔 Workout ID: {st.session_state.current_workout['workout_id']}
        📅 Time: {start_str} to {end_str}
        ━━━━━━━━━━━━━━━━━━━━━━━━━━
        📏 Distance: {st.session_state.current_workout['distance']} miles
        👣 Steps: {st.session_state.current_workout['steps']}
        🔥 Calories: {st.session_state.current_workout['calories_burned']} kcal
        📍 Start: ({st.session_state.current_workout['start_lat_lng'][0] if st.session_state.current_workout.get('start_lat_lng') else 'N/A'}, {st.session_state.current_workout['start_lat_lng'][1] if st.session_state.current_workout.get('start_lat_lng') else 'N/A'})
        """
        st.session_state.current_workout_text = details
        st.text_area("Workout Details", value=details, height=200)

else:
    st.error("Select a User To View Workouts")

workout_content = st.session_state.get('current_workout_text', '')

if workout_content:
    st.divider()
    st.subheader("Share your Results")

    if st.button("Post Workout to Feed"):
        if not st.session_state.current_user:
            st.error("Please select a user profile first.")
        else:
            image_url = get_exercise_image(workout_content)
            add_post(st.session_state.current_user, workout_content, image_url)
            st.session_state.post_success = True
            st.rerun()

if st.session_state.get("post_success"):
    st.success("Successfully posted your workout!")
    st.session_state.post_success = False