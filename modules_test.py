#############################################################################
# modules_test.py
#
# This file contains tests for modules.py.
#
# You will write these tests in Unit 2.
#############################################################################

import unittest
from streamlit.testing.v1 import AppTest
from modules import display_post, display_activity_summary, display_genai_advice, display_recent_workouts

# Write your tests below

class TestDisplayPost(unittest.TestCase):
    """Tests the display_post function."""

    def test_foo(self):
        """Tests foo."""
        pass


class TestDisplayActivitySummary(unittest.TestCase):
    """Tests the display_activity_summary function."""

    def test_activity_summary_returns_none_with_valid_workouts(self):
        """Runs display_activity_summary on valid input and confirms it returns None."""
        workouts_list = [
            {
                "workout_id": "workout0",
                "start_timestamp": "2024-01-01 00:00:00",
                "end_timestamp": "2024-01-01 00:30:00",
                "start_lat_lng": (1.2345, 4.5678),
                "end_lat_lng": (1.9876, 4.3210),
                "distance": 5.6,
                "steps": 7569,
                "calories_burned": 82,
            }
        ]

        result = display_activity_summary(workouts_list)
        self.assertIsNone(result)

    def test_activity_summary_returns_none_with_empty_list(self):
        """Empty list should not crash and should return None."""
        result = display_activity_summary([])
        self.assertIsNone(result)

    def test_activity_summary_handles_multiple_workouts_and_varied_types(self):
        """
        Uses multiple workouts including int/float/str numeric types.
        This covers the totals logic + robustness of type casting.
        """
        workouts_list = [
            {
                "workout_id": "workout0",
                "start_timestamp": "2024-01-01 00:00:00",
                "end_timestamp": "2024-01-01 00:30:00",
                "start_lat_lng": (1.1111, 4.9999),
                "end_lat_lng": (1.2222, 4.8888),
                "distance": "10.5",         # string numeric
                "steps": "1000",            # string numeric
                "calories_burned": 50,      # int
            },
            {
                "workout_id": "workout1",
                "start_timestamp": "2024-01-02 00:00:00",
                "end_timestamp": "2024-01-02 00:30:00",
                "start_lat_lng": (1.3333, 4.7777),
                "end_lat_lng": (1.4444, 4.6666),
                "distance": 2.25,           # float
                "steps": 200,               # int
                "calories_burned": "12",    # string numeric
            },
        ]

        result = display_activity_summary(workouts_list)
        self.assertIsNone(result)

    def test_activity_summary_handles_missing_optional_fields(self):
        """
        Covers the 'won't break if fields are missing' behavior.
        Missing coords should default to (0, 0) and missing numbers default to 0.
        """
        workouts_list = [
            {
                # Intentionally missing: start_lat_lng, end_lat_lng
                # Intentionally missing: distance, steps, calories_burned
                "start_timestamp": "2024-01-01 00:00:00",
                "end_timestamp": "2024-01-01 00:30:00",
            }
        ]

        result = display_activity_summary(workouts_list)
        self.assertIsNone(result)

    def test_activity_summary_coordinate_rounding_does_not_error(self):
        """
        Provides high-precision coordinates to ensure rounding logic executes without error.
        (Direct HTML verification isn't feasible here without mocking internals, but this
        ensures your rounding code path runs.)
        """
        workouts_list = [
            {
                "start_timestamp": "2024-01-01 00:00:00",
                "end_timestamp": "2024-01-01 00:30:00",
                "start_lat_lng": (1.8999999, 4.9999999),
                "end_lat_lng": (1.6944444, 4.4844444),
                "distance": 1,
                "steps": 1,
                "calories_burned": 1,
            }
        ]

        result = display_activity_summary(workouts_list)
        self.assertIsNone(result)


class TestDisplayGenAiAdvice(unittest.TestCase):
    """Tests the display_genai_advice function."""

    def test_foo(self):
        """Tests foo."""
        pass


class TestDisplayRecentWorkouts(unittest.TestCase):
    """Tests the display_recent_workouts function."""

    def test_foo(self):
        """Tests foo."""
        pass


if __name__ == "__main__":
    unittest.main()
