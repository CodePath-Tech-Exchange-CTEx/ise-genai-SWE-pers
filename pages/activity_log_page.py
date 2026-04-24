import streamlit as st
from data_fetcher import (
    add_workout,
    get_genai_advice,
    get_user_sensor_data,
    get_user_workouts,
)
from modules import require_user_selection
from datetime import datetime, date, time


# ---- Session state defaults ---- #
if "show_log_form" not in st.session_state:
    st.session_state.show_log_form = False
if "selected_workout_id" not in st.session_state:
    st.session_state.selected_workout_id = None


# ---- Helper functions ---- #

def get_user_total_stats():
    """Sums up total calories, steps and distance stats from current_user_workouts."""
    total_distance = 0.0
    total_calories = 0.0
    total_steps = 0
    if st.session_state.get("current_user_workouts"):
        for workout in st.session_state.current_user_workouts:
            total_distance += workout.get('distance') or 0
            total_calories += workout.get('calories_burned') or 0
            total_steps += workout.get('steps') or 0
    return round(total_distance, 2), round(total_calories, 2), total_steps


def format_user_stats(user_workout):
    """Reformats workout entries with cleaner names and adds duration."""
    filtered_workouts = []
    for workout_entry in user_workout:
        start = datetime.strptime(workout_entry['start_timestamp'], '%Y-%m-%d %H:%M:%S')
        end = datetime.strptime(workout_entry['end_timestamp'], '%Y-%m-%d %H:%M:%S')
        duration_minutes = int((end - start).total_seconds() / 60)
        filtered_workouts.append({
            'WorkoutId': workout_entry['workout_id'],
            'StartTimestamp': workout_entry['start_timestamp'],
            'EndTimestamp': workout_entry['end_timestamp'],
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
            if st.button("View →", key=f"view_{workout['WorkoutId']}", type="tertiary"):
                st.session_state.selected_workout_id = workout['WorkoutId']
                st.session_state.show_log_form = False
                st.rerun()
        col1.write(workout['Date'])
        col2.write(f"{workout['Duration']} min")
        col3.write(f"{workout['Distance']} km")
        col4.write(str(workout['Steps']))
        col5.write(str(workout['Calories']))


def get_workout_duration_minutes(workout):
    """Returns the workout duration in whole minutes."""
    start = datetime.strptime(workout['start_timestamp'], '%Y-%m-%d %H:%M:%S')
    end = datetime.strptime(workout['end_timestamp'], '%Y-%m-%d %H:%M:%S')
    return int((end - start).total_seconds() / 60)


def get_selected_workout():
    """Returns the selected workout from the current user's workout list."""
    selected_id = st.session_state.get("selected_workout_id")
    workouts = st.session_state.get("current_user_workouts", [])
    return next((w for w in workouts if w.get("workout_id") == selected_id), None)


def get_heart_rate_points(sensor_data):
    """Filters sensor rows down to heart-rate readings for charting."""
    heart_rate_points = []
    for sensor in sensor_data:
        sensor_type = str(sensor.get("sensor_type", "")).lower()
        if "heart" not in sensor_type:
            continue
        timestamp = sensor.get("timestamp")
        label = timestamp.strftime("%H:%M") if hasattr(timestamp, "strftime") else str(timestamp)
        heart_rate_points.append({
            "Time": label,
            "Heart Rate": sensor.get("data"),
        })
    return heart_rate_points


def render_workout_detail(workout):
    """Renders the selected workout detail view."""
    duration_minutes = get_workout_duration_minutes(workout)
    workout_date = workout['start_timestamp'].split(' ')[0]

    st.html("""
    <style>
        .block-container { padding-top: 1rem !important; }
        .detail-hero {
            background-color: #1a4fd6;
            padding: 2.5rem 2rem 2rem 2rem;
            margin-left: calc(-50vw + 50%);
            margin-right: calc(-50vw + 50%);
            margin-bottom: 1.5rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        .detail-subtitle {
            color: rgba(255,255,255,0.84);
            font-size: 1rem;
            margin: 0.5rem 0 0;
        }
    </style>
    """)

    st.html(f"""
    <div class="detail-hero">
        <h1 style="color: white !important; font-size: 2.25rem; font-weight: 700; margin: 0; padding: 0; line-height: 1;">
            {workout_date}
        </h1>
        <p class="detail-subtitle">{duration_minutes} minute workout</p>
    </div>
    """)

    calories, distance, steps = st.columns(3)
    calories.metric("Calories", workout.get("calories_burned", 0))
    distance.metric("Distance", f"{workout.get('distance', 0)} km")
    steps.metric("Steps", workout.get("steps", 0))

    sensor_data = get_user_sensor_data(
        st.session_state.current_user,
        workout["workout_id"],
    )
    heart_rate_points = get_heart_rate_points(sensor_data)
    if heart_rate_points:
        st.divider()
        st.markdown("### Heart Rate")
        st.bar_chart(heart_rate_points, x="Time", y="Heart Rate")

    st.divider()
    st.markdown("### AI Tip")
    advice = get_genai_advice(st.session_state.current_user, workout["workout_id"])
    st.info(advice.get("content", "Keep moving consistently and listen to your body."))

    st.divider()

    st.markdown("""
        <style>
            button[data-testid="stBaseButton-secondary"] {
                background-color: #2563a8 !important;
                color: white !important;
                border: none !important;
                border-radius: 20px !important;
                padding: 0.4rem 1rem !important;
            }
            button[data-testid="stBaseButton-secondary"]:hover {
                background-color: #185FA5 !important;
            }
        </style>
    """, unsafe_allow_html=True)

    if st.button("← Back to Activity Log", key="back_to_activity_log"):
        st.session_state.selected_workout_id = None
        st.rerun()

# ---- Log Workout Form ---- #

def show_log_workout_form():
    """Renders the Log a Workout form view."""
    st.html("""
    <style>
        .block-container { padding-top: 1rem !important; }
        .hero-banner-log {
            background: linear-gradient(rgba(26, 79, 214, 0.85), rgba(26, 79, 214, 0.85)),
                         url('https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=1200');
            background-size: cover;
            background-position: center;
            padding: 3rem 2rem 2.5rem 2rem;
            margin-left: calc(-50vw + 50%);
            margin-right: calc(-50vw + 50%);
            margin-bottom: 1.5rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
        }
    </style>
    <div class="hero-banner-log">
        <h1 style="color: white !important; font-size: 2.2rem; font-weight: 700; margin: 0; line-height: 1;">
            Log a workout
        </h1>
    </div>
    """)

    require_user_selection()

    st.markdown("""
    <style>
        button[data-testid="stBaseButton-primaryFormSubmit"] {
            background-color: #22c55e !important;
            color: white !important;
            border: none !important;
            border-radius: 20px !important;
        }
        button[data-testid="stBaseButton-primaryFormSubmit"]:hover {
            background-color: #16a34a !important;
        }
        button[data-testid="stBaseButton-secondaryFormSubmit"] {
            background-color: #6b7280 !important;
            color: white !important;
            border: none !important;
            border-radius: 20px !important;
        }
        button[data-testid="stBaseButton-secondaryFormSubmit"]:hover {
            background-color: #4b5563 !important;
        }
    </style>
    """, unsafe_allow_html=True)

    with st.form("log_workout_form"):
        st.markdown("**Date**")
        workout_date = st.date_input("Date", value=date.today(), label_visibility="collapsed")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Start time**")
            start_time = st.time_input("Start time", value=time(7, 0), label_visibility="collapsed")
        with col2:
            st.markdown("**End time**")
            end_time = st.time_input("End time", value=time(7, 45), label_visibility="collapsed")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Distance (km)**")
            distance = st.number_input("Distance (km)", min_value=0.0, step=0.1, format="%.1f", label_visibility="collapsed")
        with col2:
            st.markdown("**Calories**")
            calories = st.number_input("Calories", min_value=0.0, step=1.0, format="%.0f", label_visibility="collapsed")

        st.markdown("**Steps**")
        steps = st.number_input("Steps", min_value=0, step=1, label_visibility="collapsed")

        col1, col2, _ = st.columns([1, 1, 4])
        with col1:
            submitted = st.form_submit_button("Save Workout", type="primary")
        with col2:
            cancelled = st.form_submit_button("Cancel", type="secondary")

    if submitted:
        start_dt = datetime.combine(workout_date, start_time)
        end_dt = datetime.combine(workout_date, end_time)
        if end_dt <= start_dt:
            st.error("End time must be after start time.")
            return
        try:
            add_workout(
                user_id=st.session_state.current_user,
                start_timestamp=start_dt,
                end_timestamp=end_dt,
                distance=distance,
                steps=steps,
                calories=calories,
            )
            st.session_state.pop("current_user_workouts", None)
            st.session_state.show_log_form = False
            st.success("Workout saved successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"Failed to save workout: {e}")

    if cancelled:
        st.session_state.show_log_form = False
        st.rerun()


# ================================================================
# Page routing
# ================================================================

if st.session_state.show_log_form:
    show_log_workout_form()

else:
    require_user_selection()
    st.session_state.current_user_workouts = get_user_workouts(st.session_state.current_user)

    selected_workout = get_selected_workout()
    if st.session_state.selected_workout_id and selected_workout:
        render_workout_detail(selected_workout)
        st.stop()

    if st.session_state.selected_workout_id and not selected_workout:
        st.session_state.selected_workout_id = None

    # ---- Activity Log list view ---- #
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

    st.session_state.total_dist, st.session_state.total_cal, st.session_state.total_steps = get_user_total_stats()

    st.markdown(f"### {len(st.session_state.current_user_workouts)} workouts recorded")

    total_cal, total_dist, total_steps = st.columns(3)
    total_cal.metric("Total Calories Burned", st.session_state.total_cal)
    total_dist.metric("Total Distance", f"{st.session_state.total_dist}km")
    total_steps.metric("Total Steps", st.session_state.total_steps)

    st.divider()
    st.markdown("### Recent Workouts")

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
        st.session_state.show_log_form = True
        st.rerun()