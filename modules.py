#############################################################################
# modules.py
#
# This file contains modules that may be used throughout the app.
#
# You will write these in Unit 2. Do not change the names or inputs of any
# function other than the example.
#############################################################################

from internals import create_component


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
        'NAME': value,
    }
    # Register and display the component by providing the data and name
    # of the HTML file. HTML must be placed inside the "custom_components" folder.
    html_file_name = "my_custom_component"
    create_component(data, html_file_name)


def display_post(username, user_image, timestamp, content, post_image):
    """Write a good docstring here."""
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
    """Write a good docstring here."""
    pass


def display_genai_advice(timestamp, content, image):
    """Write a good docstring here."""
    pass
