#############################################################################
# pages/home.py
#
# Home page content.
#############################################################################

import streamlit as st
from modules import (
    display_genai_advice,
    display_activity_summary,
    require_user_selection,
)
from data_fetcher import get_genai_advice, get_user_workouts
from internals import create_component


# ---- Hero Banner (always visible) ---- #
create_component(
    {
        "HEADLINE": "Staying fit is hard.<br>With SWE-pers it is EASY.",
        "POINT_1": "AI-powered coaching tailored to your workouts",
        "POINT_2": "Track your distance, steps, and calories",
        "POINT_3": "Stay motivated with friends on your feed",
    },
    "hero_banner",
    height=460,
)

# ---- Dashboard (only after user selection) ---- #
require_user_selection()
user_id = st.session_state.current_user

# ---- Advice + Activity Summary side by side ---- #
col_advice, col_summary = st.columns(2)

with col_advice:
    st.subheader("Your Personalized Advice")
    with st.spinner("Generating AI advice..."):
        advice_data = get_genai_advice(user_id=user_id)
    display_genai_advice(
        advice_data.get("timestamp", ""),
        advice_data.get("content", ""),
        advice_data.get("image"),
    )

with col_summary:
    st.subheader("Activity Summary")
    with st.spinner("Loading workouts..."):
        workouts_list = get_user_workouts(user_id)
    st.caption(f"{len(workouts_list) if workouts_list else 0} workouts recorded")
    display_activity_summary(workouts_list)
