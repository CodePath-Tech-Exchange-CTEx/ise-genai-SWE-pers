import streamlit as st
from modules import display_post, require_user_selection
from data_fetcher import get_user_total_stats


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
    <h1 style="color: white !important; font-size: 2.5rem; font-weight: 700; margin: 0; padding: 0; line-height: 1;">Challenges</h1>
</div>
""")

require_user_selection()

if "total_user_stats" not in st.session_state:
    st.session_state.total_user_stats = get_user_total_stats()



# challenges_page.py

CHALLENGES = [
    {"id": "challenge1", "name": "7-day Step Challenge", "type": "Steps", "goal": 70000, "ends_in": 4, "participants": 12, "joined": True},
    {"id": "challenge2", "name": "Weekly Distance Race", "type": "Distance", "goal": 20, "ends_in": 2, "participants": 8, "joined": False},
    {"id": "challenge3", "name": "Calorie Burn-Off", "type": "Calories", "goal": 5000, "ends_in": 6, "participants": 5, "joined": False},
]

TYPE_COLORS = {
    "Steps": ("#1a3a5c", "#7ab8e8"),
    "Distance": ("#3d2e10", "#e8a84a"),
    "Calories": ("#1a3d1a", "#6dbd6d"),
}


if "challenges" not in st.session_state:
    st.session_state.challenges = CHALLENGES



def render_challenge_card(challenge, tab="all"):
    bg, fg = TYPE_COLORS[challenge["type"]]
    joined_badge = f'<span style="background:#1a3d1a; color:#6dbd6d; font-size:20px; padding:2px 8px; border-radius:10px; font-weight:500;">Joined</span>' if challenge["joined"] else "<p></p>"
  

    name = challenge['name']
    ctype = challenge['type']
    participants = challenge['participants']
    ends_in = challenge['ends_in']
    st.markdown(
    f"""
    <div style="
        border: 0.5px solid var(--color-border-tertiary);
        border-radius: 13px;
        padding: 12px 20px;
        margin-bottom: 12px;
    ">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
            <span style="font-weight:600; font-size:28px;">{name}</span>
            {joined_badge}
        </div>
        <p style="font-size:16px; color:var(--color-text-secondary); margin:0 0 8px;">
            {participants} participants · ends in {ends_in} days
        </p>
        <span style="background:{bg}; color:{fg}; font-size:16px; padding:2px 8px; border-radius:10px;">
            {ctype}
        </span>
    </div>
    """,
    unsafe_allow_html=True
)
    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("View Details", key=f"view_{challenge['id']}_{tab}"):
            st.session_state.selected_challenge = challenge
            st.switch_page("pages/challenge_detail.py")
    with col2:
        if not challenge["joined"]:
            if st.button("Quick Join", key=f"join_{challenge['id']}_{tab}"):
                st.session_state.selected_challenge = challenge
                challenge["joined"] = True
                challenge["participants"] += 1
                st.session_state.challenges = st.session_state.challenges
                st.rerun()
                

 
                

    st.divider()


st.header("Active Challenges")

tab1, tab2, tab3 = st.tabs(["All", "Mine", "Friends"])

with tab1:
    for c in st.session_state.challenges:
        render_challenge_card(c, tab="all")

with tab2:
    joined = [c for c in st.session_state.challenges if c["joined"]]
    if joined:
        for c in joined:
            render_challenge_card(c, tab="mine")
    else:
        st.info("You haven't joined any challenges yet.")

with tab3:
    st.info("Friend challenges coming soon.")