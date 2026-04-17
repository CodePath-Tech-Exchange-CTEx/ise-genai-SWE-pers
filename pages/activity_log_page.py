import streamlit as st
from data_fetcher import get_user_workouts
from modules import require_user_selection
from datetime import datetime


def get_user_total_stats():
    """Sums up total calories, steps and distance stats from current_user_workouts."""
    total_distance = 0.0
    total_calories = 0.0
    total_steps = 0
    if st.session_state.get("current_user_workouts"):
        for workout in st.session_state.current_user_workouts:
            total_distance += workout.get('distance', 0)
            total_calories += workout.get('calories_burned', 0)
            total_steps += workout.get('steps', 0)
    return round(total_distance, 2), round(total_calories, 2), total_steps


def format_user_stats(user_workout):
    """Reformats workout entries with cleaner names and adds duration."""
    filtered_workouts = []
    for workout_entry in user_workout:
        start = datetime.strptime(workout_entry['start_timestamp'], '%Y-%m-%d %H:%M:%S')
        end = datetime.strptime(workout_entry['end_timestamp'], '%Y-%m-%d %H:%M:%S')
        duration_minutes = int((end - start).total_seconds() / 60)
        filtered_workouts.append({
            'Date': workout_entry['start_timestamp'].split(' ')[0],
            'Duration': duration_minutes,
            'Distance': workout_entry['distance'],
            'Steps': workout_entry['steps'],
            'Calories': workout_entry['calories_burned'],
        })
    return filtered_workouts


def render_table(workouts):
    """Renders a workout table with View buttons."""
    st.markdown("""
    <style>
        button[data-testid="stBaseButton-tertiary"] {
            background-color: #2563a8 !important;
            color: white !important;
            border: none !important;
            border-radius: 20px !important;
            width: 100px !important;
            min-width: 100px !important;
        }
        button[data-testid="stBaseButton-tertiary"]:hover {
            background-color: #185FA5 !important;
        }
    </style>
    """, unsafe_allow_html=True)

    col0, col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 2, 2])
    col0.markdown("**View**")
    col1.markdown("**Date**")
    col2.markdown("**Duration**")
    col3.markdown("**Distance**")
    col4.markdown("**Steps**")
    col5.markdown("**Calories**")

    for workout in workouts:
        col0, col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 2, 2])
        with col0:
            if st.button("View", key=workout['Date'], type="tertiary"):
                st.session_state.selected_workout = workout
        col1.write(workout['Date'])
        col2.write(str(workout['Duration']))
        col3.write(str(workout['Distance']))
        col4.write(str(workout['Steps']))
        col5.write(str(workout['Calories']))


# ---- Page layout ---- #

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
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
</style>
<div class="hero-banner">
    <h1 style="color: white !important; font-size: 2.5rem; font-weight: 700; margin: 0; padding: 0; line-height: 1;">Activity Log</h1>
    <p style="color: rgba(255,255,255,0.8); font-size: 1rem; margin: 0.5rem 0 0;">All workouts completed to date</p>
</div>
""")

require_user_selection()

st.session_state.current_user_workouts = get_user_workouts(st.session_state.current_user)
st.session_state.total_dist, st.session_state.total_cal, st.session_state.total_steps = get_user_total_stats()



st.markdown(f"### {len(st.session_state.current_user_workouts)} workouts recorded")

total_cal,total_dist,total_steps = st.columns(3)

total_cal.metric("Total Calories Burned",st.session_state.total_cal) 
total_dist.metric("Total Distance",f"{st.session_state.total_dist}km")
total_steps.metric("Total Steps",st.session_state.total_steps)

st.divider()
st.markdown(f"### Recent Workouts")


st.markdown("""
    <style>
        button[data-testid="stBaseButton-primary"] {
            background-color: #22c55e !important;
            color: white !important;
            border: none !important;
            border-radius: 20px !important;
        }
        button[data-testid="stBaseButton-primary"]:hover {
            background-color: #16a34a !important;
        }
    </style>
""", unsafe_allow_html=True)


if st.session_state.current_user_workouts:
    render_table(format_user_stats(st.session_state.current_user_workouts))
else:
    st.info("No workouts found")

st.divider()

if st.button("Log a workout", key="log_workout", type="primary"):
    print("Logged a new workout")

