import unittest
from unittest.mock import Mock, patch
from data_fetcher import get_user_sensor_data

class TestDataFetcher(unittest.TestCase):
    """One class to hold all sensor data tests"""

    @patch('data_fetcher.client')
    def test_get_user_sensor_data(self, mock_client):
        # Setup the shared Mock for the BigQuery Job
        mock_query_job = Mock()
        mock_client.query.return_value = mock_query_job
        
        # --- TEST 1: Basic List Return ---
        mock_query_job.result.return_value = []
        result = get_user_sensor_data("user1", "workout1")
        self.assertIsInstance(result, list, "Should return a list")

        # --- TEST 2: SQL Injection Check ---
        workout_id = "test_123"
        get_user_sensor_data("user1", workout_id)
        called_sql = mock_client.query.call_args[0][0]
        self.assertIn(f"t1.WorkoutID = '{workout_id}'", called_sql)

        # --- TEST 3: Row Mapping ---
      
        row_data = {"SensorName": "Heart Rate", "SensorValue": 100.0}

        mock_row = Mock()
        mock_row.items.return_value = row_data.items()
        mock_row.__getitem__ = Mock(side_effect=lambda key: row_data[key])

        # ADD THIS — makes row.SensorName, row.SensorValue, etc. work
        mock_row.configure_mock(**{
            "SensorName": "Heart Rate",
            "SensorValue": 100.0,
            "Timestamp": None,
            "Units": None
        })

        mock_query_job.result.return_value = [mock_row]
        result = get_user_sensor_data("user1", "workout1")

        self.assertEqual(result[0]["sensor_type"], "Heart Rate")
        self.assertEqual(result[0]["data"], 100.0)

        # --- TEST 4: Empty Results ---
        mock_query_job.result.return_value = []
        self.assertEqual(get_user_sensor_data("u", "w"), [])

        # --- TEST 5: Multiple Rows ---
        mock_query_job.result.return_value = [Mock(), Mock(), Mock()]
        self.assertEqual(len(get_user_sensor_data("u", "w")), 3)

if __name__ == "__main__":
    unittest.main()