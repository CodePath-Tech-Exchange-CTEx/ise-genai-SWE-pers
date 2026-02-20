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
    pass


def display_activity_summary(workouts_list):
    """Write a good docstring here."""
    pass


def display_recent_workouts(workouts_list):
    """Function takes in a list of user workouts and displays the full workout information
       params: A list of user_workout info
       returns: None
    """

    #Take in the workout list and diaply just the workout names
    if "view_option" not in st.session_state:
        st.session_state.view_option = "View More"

    if "workout_option_index" not in st.session_state:
        st.session_state.workout_option_index = 0

    if "show_area" not in st.session_state:
        st.session_state.show_area = False


    if workouts_list:

        workout_options =  ["select an option"] + [workout["workout_id"] for workout in workouts_list]

        workout_id = st.selectbox("Select a Workout", options = workout_options, key="selected_workout_id")

        st.session_state.workout_option_index = 0 if workout_id not in workout_options else workout_options.index(workout_id)
        

        def handle_view_option():
            if "view_option" in st.session_state:
                if  st.session_state.view_option != "View Less":
                    st.session_state.view_option = "View Less"
                    st.session_state.show_area = True
                    
                else:
                    st.session_state.view_option = "View More"
                    st.session_state.show_area = False

        view_option = st.button(f"{st.session_state.view_option}", on_click=handle_view_option)
        
        if st.session_state.show_area:
            if workout_id == "select an option":
                st.warning("Please select a workout from the dropdown first.")
            
            else:
                text = ""
                for key, val in workouts_list[st.session_state.workout_option_index-1].items():
                    text += key + ": " + str(val) + "\n"

                st.text_area(label= "Text" ,value = text,label_visibility="hidden")

    else:
        st.subheader(":red[You Have No Workouts]")
    

    


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
