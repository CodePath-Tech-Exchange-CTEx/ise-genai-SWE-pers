#############################################################################
# pages/home.py
#
# Home page content.
#############################################################################

import streamlit as st
from modules import display_post, display_genai_advice, display_activity_summary
from data_fetcher import get_genai_advice, get_user_workouts, get_post
from internals import create_component


# ---- Hero Banner ---- #
create_component({
    "HEADLINE": "Staying fit is hard.<br>With SWE-pers it is EASY.",
    "POINT_1": "AI-powered coaching tailored to your workouts",
    "POINT_2": "Track your distance, steps, and calories",
    "POINT_3": "Stay motivated with friends on your feed",
    "FOOTER_TEXT": "<- Select a user from the sidebar to get started.",
}, "hero_banner", height=460)


# ---- Dashboard (only if user selected) ---- #
user_id = st.session_state.get("current_user")
if not user_id:
    st.stop()

# ---- Personalized Advice ---- #
st.subheader("Your Personalized Advice")
advice_data = get_genai_advice(user_id=user_id)
display_genai_advice(
    advice_data.get("timestamp", ""),
    advice_data.get("content", ""),
    advice_data.get("image"),
)

st.divider()

# ---- Activity Summary ---- #
workouts_list = get_user_workouts(user_id)
st.caption(f"Loaded workouts: {len(workouts_list) if workouts_list else 0}")
display_activity_summary(workouts_list)

st.divider()

# ---- Most Recent Post ---- #
post_data = get_post(user_id)
display_post(
    post_data['username'],
    post_data['user_image'],
    post_data['timestamp'],
    post_data['content'],
    post_data.get('image_url'),
)
