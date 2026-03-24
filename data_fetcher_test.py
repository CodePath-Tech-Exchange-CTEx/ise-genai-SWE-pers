#############################################################################
# data_fetcher_test.py
#
# This file contains tests for data_fetcher.py.
#
# You will write these tests in Unit 3.
#############################################################################
import unittest
from unittest.mock import patch, MagicMock
from data_fetcher import get_user_workouts

class TestDataFetcher(unittest.TestCase):

    @patch("data_fetcher.bq_client.query")
    def test_get_user_workouts_success(self, mock_query):
        """Tests that get_user_workouts correctly maps BigQuery results to a list of dicts."""
        mock_job = MagicMock()
        mock_row1 = MagicMock()
        mock_row1.items.return_value = [
            ("WorkoutId", "w1"),
            ("StartTimestamp", "2024-01-01 08:00:00"),
            ("EndTimestamp", "2024-01-01 09:00:00"),
            ("StartLocationLat", 1.0),
            ("StartLocationLong", 2.0),
            ("EndLocationLat", 3.0),
            ("EndLocationLong", 4.0),
            ("TotalDistance", 5.0),
            ("TotalSteps", 6000),
            ("CaloriesBurned", 400),
        ]
        mock_job.result.return_value = [mock_row1]
        mock_query.return_value = mock_job

        workouts = get_user_workouts("user1")
        
        self.assertEqual(len(workouts), 1)
        workout = workouts[0]
        self.assertEqual(workout["workout_id"], "w1")
        self.assertEqual(workout["start_timestamp"], "2024-01-01 08:00:00")
        self.assertEqual(workout["end_timestamp"], "2024-01-01 09:00:00")
        self.assertEqual(workout["start_lat_lng"], (1.0, 2.0))
        self.assertEqual(workout["end_lat_lng"], (3.0, 4.0))
        self.assertEqual(workout["distance"], 5.0)
        self.assertEqual(workout["steps"], 6000)
        self.assertEqual(workout["calories_burned"], 400)
        mock_query.assert_called_once()

    @patch("data_fetcher.bq_client.query")
    def test_get_user_workouts_empty(self, mock_query):
        """Tests that get_user_workouts returns an empty list when no records match."""
        mock_job = MagicMock()
        mock_job.result.return_value = []
        mock_query.return_value = mock_job

        workouts = get_user_workouts("user2")
        self.assertEqual(workouts, [])
        mock_query.assert_called_once()

    @patch("data_fetcher.bq_client.query")
    def test_get_user_workouts_missing_fields(self, mock_query):
        """Tests that get_user_workouts gracefully handles missing optional fields."""
        mock_job = MagicMock()
        mock_row1 = MagicMock()
        mock_row1.items.return_value = [("WorkoutId", "w2")]
        mock_job.result.return_value = [mock_row1]
        mock_query.return_value = mock_job

        workouts = get_user_workouts("user3")
        self.assertEqual(len(workouts), 1)
        self.assertEqual(workouts[0]["workout_id"], "w2")
        self.assertIsNone(workouts[0]["start_timestamp"])
        self.assertIsNone(workouts[0]["distance"])

if __name__ == "__main__":
    unittest.main()