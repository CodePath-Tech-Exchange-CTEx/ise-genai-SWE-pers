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

# Replace Deploy button with GitHub link styled to match the 3-dot menu button
st.markdown("""
<style>
    [data-testid="stAppDeployButton"] { display: none; }
    .block-container { padding-top: 4rem !important; }
    .hero-banner, .hero-banner-log { min-height: 250px; }
    .github-header-btn {
        position: fixed;
        top: 1rem;
        right: 3.8rem;
        z-index: 999999;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 32px;
        height: 29px;
        padding: 0;
        border: none;
        background: none;
        cursor: pointer;
    }
    .github-header-btn svg {
        fill: rgb(250, 250, 250);
        width: 18px;
        height: 18px;
    }
    .github-header-btn:hover {
        background-color: rgba(250, 250, 250, 0.1);
        border-radius: 0.5rem;
    }
</style>
<a class="github-header-btn" href="https://github.com/CodePath-Tech-Exchange-CTEx/ise-genai-SWE-pers" target="_blank" title="GitHub">
    <svg viewBox="0 0 16 16"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8z"/></svg>
</a>
""", unsafe_allow_html=True)

# ---- Pages & navigation (hidden auto-nav so we control sidebar order) ---- #
home = st.Page("pages/home.py", title="Home", icon="🏠", default=True)
# activity = st.Page("pages/activity_page.py", title="Activity", icon="🏃")  # TODO: merge sharing into Activity Log or repurpose as detail view
activity_log = st.Page("pages/activity_log_page.py", title="Activity Log", icon="📊")
community = st.Page("pages/community_page.py", title="Community", icon="👥")

pg = st.navigation([home, activity_log, community], position="hidden")

# ---- Sidebar: Branding → User Selector → Nav links ---- #
with st.sidebar:
    st.header("💪 SWE-pers")
    st.divider()

    user_list = st.session_state.user_list
    current = st.session_state.get("current_user", "")

    options = ["Select a User"] + sorted(user_list)
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

    st.page_link(home, label="Home", icon=":material/home:")
    # st.page_link(activity, label="Activity", icon=":material/directions_run:")  # TODO
    st.page_link(activity_log, label="Activity Log", icon=":material/bar_chart:")
    st.page_link(community, label="Community", icon=":material/group:")

pg.run()
