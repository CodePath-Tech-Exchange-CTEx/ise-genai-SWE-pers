#############################################################################
# app.py
#
# Central router. Sets up the sidebar (branding + user selector) then
# hands off to whichever page the user navigates to via st.navigation().
#############################################################################

import streamlit as st


st.set_page_config(
    page_title="SWE-pers",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded",
)

from data_fetcher import get_users

# ---- Session state defaults ---- #
if "current_user" not in st.session_state:
    st.session_state.current_user = ""
if "user_list" not in st.session_state:
    st.session_state.user_list = get_users()

# ---- Sidebar: Branding → User Selector (appears ABOVE nav links) ---- #
with st.sidebar:
    st.markdown("## 💪 SWE-pers")
    st.caption("Social Workout Experience")
    st.divider()

    user_list = st.session_state.user_list
    current = st.session_state.get("current_user", "")

    options = ["Select a User"] + user_list
    current_index = (user_list.index(current) + 1) if current in user_list else 0

    selected = st.selectbox(
        "Active User", options, index=current_index, key="sidebar_user_selector"
    )

    if selected != "Select a User" and selected != current:
        st.session_state.current_user = selected
        # Clear cached workout data when user changes
        st.session_state.pop("current_user_workouts", None)
        st.rerun()

    if current:
        st.success(f"Logged in as **{current}**")

    st.divider()

# ---- Navigation (renders nav links in sidebar below the content above) ---- #
home = st.Page("pages/home.py", title="Home", icon="🏠", default=True)
activity = st.Page("pages/activity_page.py", title="Activity", icon="🏃")
activity_log = st.Page("pages/activity_log_page.py", title="Activity Log", icon="📊")
community = st.Page("pages/community_page.py", title="Community", icon="👥")

pg = st.navigation([home, activity, activity_log, community])
pg.run()

value = st.session_state.current_user




