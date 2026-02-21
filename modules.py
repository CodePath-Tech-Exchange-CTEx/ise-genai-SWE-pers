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
    """Write a good docstring here."""
    pass


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
