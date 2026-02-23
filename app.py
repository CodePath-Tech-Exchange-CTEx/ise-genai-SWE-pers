#############################################################################
# app.py
#
# This file contains the entrypoint for the app.
#
#############################################################################

import streamlit as st
from modules import display_my_custom_component, display_post, display_genai_advice, display_activity_summary, display_recent_workouts
from data_fetcher import get_user_posts, get_genai_advice, get_user_profile, get_user_sensor_data, get_user_workouts, get_post

userId = 'user1'
data = get_genai_advice(user_id=userId)

def render_genai_section(user_id):
    """Fetches and displays the GenAI advice component."""
    # 1. Fetch the data inside the function
    advice_data = get_genai_advice(user_id=user_id)
    
    # 2. Extract values with safety defaults
    timestamp = advice_data.get("timestamp", "No Date Known...")
    content = advice_data.get("content", "No Content Known...")
    image = advice_data.get("image") # modules.py will handle the None fallback
    
    # 3. Call the display module
    display_genai_advice(timestamp, content, image)


def display_app_page():
    """Displays the home page of the app."""
    st.title('Welcome to SDS!')

    # An example of displaying a custom component called "my_custom_component"
    value = st.text_input('Enter your name')
    display_my_custom_component(value)
    st.divider() # Optional: adds a visual line between sections
    st.subheader("Your Personalized Advice")
    render_genai_section(userId)
    post_data = get_post('user5')
    
    
    if "user_workouts" not in st.session_state:
        st.session_state.user_workouts = get_user_workouts("random_user_id")
    
    display_recent_workouts(st.session_state.user_workouts)
    # display_recent_workouts([])
    # display_recent_workouts(None)

    # ---- Activity Summary ---- #
    workouts_list = get_user_workouts(userId)

    # Shows how many workouts were loaded
    st.caption(f"Loaded workouts: {len(workouts_list) if workouts_list else 0}")

    display_activity_summary(workouts_list)


    # displays a post with dummy data
    display_post(post_data['username'], post_data['user_image'], post_data['timestamp'], post_data['content'], post_data['post_image'])
# This is the starting point for your app. You do not need to change these lines
if __name__ == '__main__':
    display_app_page()
