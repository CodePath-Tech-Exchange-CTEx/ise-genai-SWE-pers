#############################################################################
# pages/home.py
#
# Home page content.
#############################################################################

import streamlit as st
from modules import display_post, display_genai_advice, display_activity_summary, require_user_selection
from data_fetcher import get_genai_advice, get_user_workouts, get_post


# ---- Hero Banner ---- #
st.html("""
<style>
    .block-container { padding-top: 1rem !important; }
    .hero-banner {
        background-color: #1a4fd6;
        padding: 4rem 2rem 3rem 2rem;
        margin-left: calc(-50vw + 50%);
        margin-right: calc(-50vw + 50%);
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }
</style>
<div class="hero-banner">
    <h1 style="color: white !important; font-size: 2.5rem; font-weight: 700; margin: 0; padding: 0; line-height: 1;">Welcome to SDS</h1>
</div>
""")

require_user_selection()

user_id = st.session_state.current_user

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
