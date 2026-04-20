# leaderboard_extras.py
import streamlit as st

METRIC_KEY = {
    "Steps": "GrandTotalSteps",
    "Distance": "GrandTotalDistance",
    "Calories": "GrandTotalCalories",
}
METRIC_UNIT = {
    "Steps": "steps",
    "Distance": "km",
    "Calories": "cal",
}

TYPE_COLORS = {
    "Steps": ("#1a3a5c", "#7ab8e8"),
    "Distance": ("#3d2e10", "#e8a84a"),
    "Calories": ("#1a3d1a", "#6dbd6d"),
}

def get_user_progress(user_id, challenge_type, leaderboard_data):
    """Gets current user's metric from leaderboard data."""
    key = METRIC_KEY[challenge_type]
    for entry in leaderboard_data:
        if entry["UserId"] == user_id:
            return entry[key]
    return 0

def display_progress_view(challenge, user_id, leaderboard_data):
    """Displays the user's progress against the challenge goal."""
    challenge_type = challenge["type"]
    goal = challenge["goal"]
    progress = get_user_progress(user_id, challenge_type, leaderboard_data)
    unit = METRIC_UNIT[challenge_type]
    percent = min(int((progress / goal) * 100), 100) if goal else 0
    bg, fg = TYPE_COLORS[challenge_type]
    name = challenge["name"]
    participants = challenge["participants"]
    ends_in = challenge["ends_in"]
    joined_badge = '<span style="background:#1a3d1a; color:#6dbd6d; font-size:20px; padding:2px 8px; border-radius:10px; font-weight:500;">Joined</span>' if challenge["joined"] else "<p></p>"
    type_badge = f'<span style="background:{bg}; color:{fg}; font-size:20px; padding:2px 8px; border-radius:10px;">{challenge_type}</span>'

    st.markdown(f"""
        <div style="margin-bottom:12px;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
                <span style="font-weight:600; font-size:24px;">{name}</span>
                {joined_badge}
                {type_badge}
            </div>
            <p style="font-size:18px; color:rgba(255,255,255,0.6); margin:0;">{participants} participants · ends in {ends_in} days</p>
        </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("**Your Progress**")
    st.markdown(f"""
        <div style="margin-bottom:8px;">
            <div style="display:flex; justify-content:space-between; font-size:21px; margin-bottom:6px;">
                <span style="font-weight:500;">{progress:,} {unit}</span>
                <span style="color:rgba(255,255,255,0.6);">Goal: {goal:,} {unit}</span>
            </div>
            <div style="background:rgba(255,255,255,0.1); border-radius:4px; height:10px;">
                <div style="background:#2563a8; width:{percent}%; height:10px; border-radius:4px;"></div>
            </div>
            <p style="font-size:19px; color:rgba(255,255,255,0.6); margin-top:6px;">{percent}% completed</p>
        </div>
    """, unsafe_allow_html=True)

    st.divider()
    if not challenge.get("joined"):
        if st.button("Join Challenge", key="join_challenge", type="primary"):
            challenge["joined"] = True
            st.session_state.selected_challenge = challenge
            # update in challenges list too
            for c in st.session_state.challenges:
                if c["id"] == challenge["id"]:
                    c["joined"] = True
            st.session_state.just_joined = True
            st.rerun()

    if st.session_state.get("just_joined"):
        st.success("Lets Go! You have joined the challenge")
        st.session_state.just_joined = False

   


def display_leaderboard_view(challenge, user_id, leaderboard_data):
    """Displays ranked leaderboard with current user highlighted."""
    challenge_type = challenge["type"]
    key = METRIC_KEY[challenge_type]
    unit = METRIC_UNIT[challenge_type]
    bg, fg = TYPE_COLORS[challenge_type]
    name = challenge["name"]
    joined_badge = '<span style="background:#1a3d1a; color:#6dbd6d; font-size:20px; padding:2px 8px; border-radius:10px; font-weight:500;">Joined</span>' if challenge["joined"] else "<p></p>"
    type_badge = f'<span style="background:{bg}; color:{fg}; font-size:20px; padding:2px 8px; border-radius:10px;">{challenge_type}</span>'

    sorted_data = sorted(leaderboard_data, key=lambda x: x[key], reverse=True)
    user_rank = next((i + 1 for i, e in enumerate(sorted_data) if e["UserId"] == user_id), None)

    user_metric = get_user_progress(user_id, challenge_type, leaderboard_data)

    st.markdown(f"""
        <div style="margin-bottom:12px;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
                <span style="font-weight:600; font-size:24px;">{name}</span>
                {joined_badge}
                {type_badge}
            </div>
            <p style="font-size:20px; color:rgba(255,255,255,0.6); margin:0;">You are currently ranked #{user_rank}</p>
            <p style="font-size:19px; margin:4px 0 0;">Your {challenge_type}: <span style="font-size:2 rem; font-weight:700;">{user_metric:,} {unit}</span></p>
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    for i, entry in enumerate(sorted_data):
        is_you = entry["UserId"] == user_id
        metric_val = entry[key]
        rank = i + 1
        metric_val = entry[key]
        bg_row = "background:rgba(37,99,168,0.3);" if is_you else ""
        label = "You" if is_you else entry["UserId"]
        st.markdown(f"""
            <div style="
                display:flex; align-items:center;
                padding:10px 14px; border-radius:8px;
                margin-bottom:6px; {bg_row}
                border: 0.5px solid rgba(255,255,255,0.1);
            ">
                <span style="font-size:25px; font-weight:500; min-width:32px; color:rgba(255,255,255,0.6);">#{rank}</span>
                <span style="font-size:25px; flex:1; {'font-weight:700; color:#7ab8e8;' if is_you else ''}">{label}</span>
                <span style="font-size:25px; font-weight:500; {'color:#7ab8e8;' if is_you else ''}">{metric_val:,}</span>
            </div>
        """, unsafe_allow_html=True)

    st.divider()

    if st.button("← Back to Progress", key="back_to_progress"):
        st.session_state.show_leaderboard = False
        st.rerun()