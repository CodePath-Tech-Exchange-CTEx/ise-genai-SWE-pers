#############################################################################
# modules.py
#
# This file contains modules that may be used throughout the app.
#
# You will write these in Unit 2. Do not change the names or inputs of any
# function other than the example.
#############################################################################

from internals import create_component
import streamlit as st


# This one has been written for you as an example. You may change it as wanted.
def display_my_custom_component(value):
    """Displays a 'my custom component' which showcases an example of how custom
    components work.

    value: the name you'd like to be called by within the app
    """
    # Define any templated data from your HTML file. The contents of
    # 'value' will be inserted to the templated HTML file wherever '{{NAME}}'
    # occurs. You can add as many variables as you want.
    data = {
        "NAME": value,
    }
    # Register and display the component by providing the data and name
    # of the HTML file. HTML must be placed inside the "custom_components" folder.
    html_file_name = "my_custom_component"
    create_component(data, html_file_name)


def display_post(username, user_image, timestamp, content, post_image):
    """Write a good docstring here."""
    col1, col2 = st.columns([1,9])
    with col1:
        st.image(user_image, width=50)
    with col2:
        st.text(username)
    st.image(post_image, width=700)
    st.markdown(
    f"""
    <div style="
        text-align: right;
        width: 100%;
        font-size: 12px;
        color: #888;
        margin-top: 4px;
    ">
        {timestamp}
    </div>
    """,
    unsafe_allow_html=True
)
    st.text(username + ":  " + content)
    
    
    pass


def display_activity_summary(workouts_list):
    """Displays an activity summary section for a list of workouts.

    Input:
        workouts_list: list of workout dictionaries. Each workout contains:
            - start_timestamp, end_timestamp
            - distance, steps, calories_burned
            - start_coordinates, end_coordinates

    Output:
        None (renders a custom HTML component on the app)
    """
    workouts_list = workouts_list or []

    # ---- totals ----
    total_workouts = len(workouts_list)
    total_distance = 0.0
    total_steps = 0
    total_calories = 0.0

    for w in workouts_list:
        total_distance += float(w.get("distance", 0) or 0)
        total_steps += int(w.get("steps", 0) or 0)
        total_calories += float(w.get("calories_burned", 0) or 0)

    # ---- Builds a simple HTML list/table for workouts ---- #
    # Keep it lightweight so it won't break if some fields are missing.
    rows_html = ""
    for w in workouts_list:
        start_ts = str(w.get("start_timestamp", ""))
        end_ts = str(w.get("end_timestamp", ""))
        dist = w.get("distance", 0)
        steps = w.get("steps", 0)
        cal = w.get("calories_burned", 0)
        start_coordinates = w.get("start_lat_lng", (0, 0))
        end_coordinates = w.get("end_lat_lng", (0, 0))

        # To format the coordinates and round them to two decimal places
        start_coordinates = (
            round(float(start_coordinates[0]), 2),
            round(float(start_coordinates[1]), 2)
        )

        end_coordinates = (
            round(float(end_coordinates[0]), 2),
            round(float(end_coordinates[1]), 2)
        )


        rows_html += f"""
        <tr>
            <td>{start_ts}</td>
            <td>{end_ts}</td>
            <td>{dist}</td>
            <td>{steps}</td>
            <td>{cal}</td>
            <td>{start_coordinates}</td>
            <td>{end_coordinates}</td>
        </tr>
        """

    if not rows_html:
        rows_html = """
        <tr>
            <td colspan="7" style="text-align:center; opacity:0.8;">
                No workouts yet.
            </td>
        </tr>
        """

    # ---- Templated data for the HTML component ---- #
    data = {
        "TOTAL_WORKOUTS": str(total_workouts),
        "TOTAL_DISTANCE": f"{total_distance:.2f}",
        "TOTAL_STEPS": str(total_steps),
        "TOTAL_CALORIES": f"{total_calories:.1f}",
        "WORKOUT_ROWS": rows_html,
    }

    # Name of the HTML file inside /custom_components (no .html extension)
    html_file_name = "activity_summary"
    create_component(data, html_file_name, height=900, scrolling=True)


def display_recent_workouts(workouts_list):
    """Function takes in a list of user workouts and displays the full workout information
       params: A list of user_workout info
       returns: None
    """
    
    import streamlit as st

def display_recent_workouts(workouts_list):
    # 1. Initialize visibility state
    if "show_area" not in st.session_state:
        st.session_state.show_area = False

    if not workouts_list:
        st.subheader(":red[You Have No Workouts]")
        return

    # The Selection 
    workout_ids = ["select an option"] + [w["workout_id"] for w in workouts_list]
    selected_id = st.selectbox("Select a Workout", options=workout_ids, key="selected_workout_id")

    #oggle Button
    def handle_view_option_click():
        st.session_state.show_area = not st.session_state.show_area

    view_option = st.button("View More" if not st.session_state.show_area else "View Less", key="view_option_button",on_click=handle_view_option_click)
        

    # Immediate Render Logic
    if st.session_state.show_area:
        # Find the workout object immediately based on the selectbox's current value
        workout = next((w for w in workouts_list if w["workout_id"] == selected_id), None)
        
        if workout:
           
            workout_info = (
                f"ID: {workout['workout_id']}\n"
                f"Start: {workout['start_timestamp']}\n"
                f"End: {workout['end_timestamp']}\n"
                f"Dist: {workout['distance']} km\n"
                f"Steps: {workout['steps']}\n"
                f"Calories: {workout['calories_burned']}"
            )
            
            st.text_area("Workout Details", value=workout_info, height=200, disabled=True,key="workout_text_area")
    
        else:
           st.warning("Please select a workout from the dropdown first.") 
    


def display_genai_advice(timestamp, content, image):
    """Displays a 'my custom component' which showcases an example of how custom
    components work.

    value: the name you'd like to be called by within the app
    """
    # Define any templated data from your HTML file. The contents of
    # 'value' will be inserted to the templated HTML file wherever '{{NAME}}'
    # occurs. You can add as many variables as you want.
    if image is None or image == "No Image Known...":
        image = "https://placehold.co/600x400?text=Keep+Going!"

    data = {"timestamp": timestamp, "content": content, "image": image}

    # --- HEIGHT LOGIC ---
    # Base height for image and timestamp is ~450px
    # We add ~25px for every 100 characters of text content
    estimated_height = 600 + (len(content) // 4)

    # Register and display the component by providing the data and name
    # of the HTML file. HTML must be placed inside the "custom_components" folder.
    html_file_name = "genai_advice"
    create_component(data, html_file_name, height=estimated_height)
