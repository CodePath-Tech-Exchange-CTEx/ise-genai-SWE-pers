#############################################################################
# app.py
#
# This file contains the entrypoint for the app.
#
#############################################################################

import streamlit as st
from modules import display_my_custom_component, display_post, display_genai_advice, display_activity_summary, display_recent_workouts
from data_fetcher import get_user_posts, get_genai_advice, get_user_profile, get_user_sensor_data, get_user_workouts

userId = 'user1'


def display_app_page():
    """Displays the home page of the app."""
    st.title('Welcome to SDS!')

    # An example of displaying a custom component called "my_custom_component"
    value = st.text_input('Enter your name')
    display_my_custom_component(value)
    
    if "user_workouts" not in st.session_state:
        st.session_state.user_workouts = get_user_workouts("random_user_id")
    
    display_recent_workouts(st.session_state.user_workouts)
    # display_recent_workouts([])
    # display_recent_workouts(None)

# This is the starting point for your app. You do not need to change these lines
if __name__ == '__main__':
    display_app_page()
