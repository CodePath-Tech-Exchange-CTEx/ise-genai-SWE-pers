#############################################################################
# modules_test.py
#
# This file contains tests for modules.py.
#
# You will write these tests in Unit 2.
#############################################################################

import unittest
from streamlit.testing.v1 import AppTest
from modules import (
    display_post,
    display_activity_summary,
    display_genai_advice,
    display_recent_workouts,
)

# Write your tests below


class TestDisplayPost(unittest.TestCase):
    """Tests the display_post function."""

    def test_foo(self):
        """Tests foo."""
        pass


class TestDisplayActivitySummary(unittest.TestCase):
    """Tests the display_activity_summary function."""

    def test_foo(self):
        """Tests foo."""
        pass


class TestDisplayGenAiAdvice(unittest.TestCase):
    """Tests the display_genai_advice function."""

    def test_genai_loads(self):
        # 1. Create a wrapper function that IMPORTS the module inside it.
        # This ensures the global dependencies in modules.py are loaded.
        def run_genai_module():
            from modules import display_genai_advice

            display_genai_advice(
                "2024-01-01 00:00:00",
                "Your heart rate indicates you can push yourself further. You got this!",
                None,
            )

        # 2. Pass the wrapper function to AppTest
        at = AppTest.from_function(run_genai_module)
        at.run()

        # 3. Assert no exceptions occurred
        self.assertFalse(at.exception)


class TestDisplayRecentWorkouts(unittest.TestCase):
    """Tests the display_recent_workouts function."""

    def test_recent_workout_select_workout(self):
        at = AppTest.from_file("app.py")
        at.run()

        # Test for the first workout
        at.selectbox(key="selected_workout_id").set_value("workout0")
        at.button(key="view_option_button").click()
        at.run()

        text_area = at.text_area(key="workout_text_area")
        assert "workout0" in text_area.value

    def test_recent_workout_select_an_option(self):
        at = AppTest.from_file("app.py")
        at.run()

        #Test for "select an option"
   
        at.selectbox(key="selected_workout_id").set_value("select an option")
        at.button(key="view_option_button").click()
        at.run()

        warnings = at.warning
        assert len(warnings) > 0
        assert "Please select a workout" in warnings[0].value


if __name__ == "__main__":
    unittest.main()
