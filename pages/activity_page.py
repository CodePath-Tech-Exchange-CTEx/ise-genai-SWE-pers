import streamlit as st
from data_fetcher import get_user_workouts, get_exercise_image, add_post
from modules import require_user_selection


if 'current_user_workouts' not in st.session_state:
    st.session_state.current_user_workouts = []


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
    <h1 style="color: white !important; font-size: 2.5rem; font-weight: 700; margin: 0; padding: 0; line-height: 1;">Activity Page</h1>
</div>
""")

require_user_selection()

st.divider()

if st.session_state.current_user:
    if not st.session_state.current_user_workouts:
        st.session_state.current_user_workouts = get_user_workouts(st.session_state.current_user)

    st.subheader("Workout History")

    for workout in st.session_state.current_user_workouts[:3]:
        if st.button(workout["workout_id"], key=workout["workout_id"]):
            st.session_state.current_workout = workout

    if st.session_state.get("current_workout"):
        start_str = st.session_state.current_workout['start_timestamp'][:16]
        end_str = st.session_state.current_workout['end_timestamp'][11:16]

        # Lines written by GEMINI
        details = f"""
        🆔 Workout ID: {st.session_state.current_workout['workout_id']}
        📅 Time: {start_str} to {end_str}
        ━━━━━━━━━━━━━━━━━━━━━━━━━━
        📏 Distance: {st.session_state.current_workout['distance']} miles
        👣 Steps: {st.session_state.current_workout['steps']}
        🔥 Calories: {st.session_state.current_workout['calories_burned']} kcal
        📍 Start: ({st.session_state.current_workout['start_lat_lng'][0] if st.session_state.current_workout.get('start_lat_lng') else 'N/A'}, {st.session_state.current_workout['start_lat_lng'][1] if st.session_state.current_workout.get('start_lat_lng') else 'N/A'})
        """
        st.session_state.current_workout_text = details
        st.text_area("Workout Details", value=details, height=200)

else:
    st.error("Select a User To View Workouts")

workout_content = st.session_state.get('current_workout_text', '')

if workout_content:
    st.divider()
    st.subheader("Share your Results")

    if st.button("Post Workout to Feed"):
        if not st.session_state.current_user:
            st.error("Please select a user profile first.")
        else:
            image_url = get_exercise_image(workout_content)
            add_post(st.session_state.current_user, workout_content, image_url)
            st.session_state.post_success = True
            st.rerun()

if st.session_state.get("post_success"):
    st.success("Successfully posted your workout!")
    st.session_state.post_success = False