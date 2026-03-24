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
from datetime import datetime


class TestDataFetcher(unittest.TestCase):

    @patch("data_fetcher.bigquery.Client")
    def test_get_user_workouts_success(self, MockClient):
        """Tests that get_user_workouts correctly maps BigQuery results to a list of dicts."""
        mock_client_instance = MockClient.return_value
        mock_query = mock_client_instance.query
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

    @patch("data_fetcher.bigquery.Client")
    def test_get_user_workouts_empty(self, MockClient):
        """Tests that get_user_workouts returns an empty list when no records match."""
        mock_client_instance = MockClient.return_value
        mock_query = mock_client_instance.query
        mock_job = MagicMock()
        mock_job.result.return_value = []
        mock_query.return_value = mock_job

        workouts = get_user_workouts("user2")
        self.assertEqual(workouts, [])
        mock_query.assert_called_once()

    @patch("data_fetcher.bigquery.Client")
    def test_get_user_workouts_missing_fields(self, MockClient):
        """Tests that get_user_workouts gracefully handles missing optional fields."""
        mock_client_instance = MockClient.return_value
        mock_query = mock_client_instance.query
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

class TestGetGenaiAdvice(unittest.TestCase):
    """Tests the get_genai_advice function."""
 
    def setUp(self):
        """Import the function under test inside setUp so each test is isolated."""
        from data_fetcher import get_genai_advice  # Line written by Claude
        self.get_genai_advice = get_genai_advice  # Line written by Claude
        
        # Mock BigQuery Client to prevent real API calls during GenAI tests
        patcher = patch("data_fetcher.bigquery.Client")
        self.mock_bq_client = patcher.start()
        self.addCleanup(patcher.stop)
 
    def test_returns_dict(self):
        """Tests that get_genai_advice returns a dictionary."""
        result = self.get_genai_advice("user1")  # Line written by Claude
        self.assertIsInstance(result, dict)  # Line written by Claude
 
    def test_has_required_keys(self):
        """Tests that the returned dictionary contains all required keys."""
        result = self.get_genai_advice("user1")  # Line written by Claude
        required_keys = ["advice_id", "timestamp", "content", "image"]  # Line written by Claude
        for key in required_keys:  # Line written by Claude
            self.assertIn(key, result, f"Missing required key: {key}")  # Line written by Claude
 
    def test_content_is_non_empty_string(self):
        """Tests that content is a non-empty string."""
        result = self.get_genai_advice("user1")  # Line written by Claude
        self.assertIsInstance(result["content"], str)  # Line written by Claude
        self.assertTrue(len(result["content"]) > 0, "Content should not be empty")  # Line written by Claude
 
    def test_timestamp_is_valid_format(self):
        """Tests that the timestamp follows YYYY-MM-DD HH:MM:SS format."""
        result = self.get_genai_advice("user1")  # Line written by Claude
        timestamp = result["timestamp"]  # Line written by Claude
        self.assertIsInstance(timestamp, str)  # Line written by Claude
        # Should not raise if format is correct  # Line written by Claude
        try:
            datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")  # Line written by Claude
        except ValueError:  # Line written by Claude
            self.fail(f"Timestamp '{timestamp}' is not in expected format YYYY-MM-DD HH:MM:SS")  # Line written by Claude
 
    def test_advice_id_contains_user_id(self):
        """Tests that the advice_id includes the user_id for traceability."""
        user_id = "user1"  # Line written by Claude
        result = self.get_genai_advice(user_id)  # Line written by Claude
        self.assertIsInstance(result["advice_id"], str)  # Line written by Claude
        self.assertIn(user_id, result["advice_id"], "advice_id should contain the user_id")  # Line written by Claude
 
    def test_advice_id_is_non_empty_string(self):
        """Tests that advice_id is a non-empty string."""
        result = self.get_genai_advice("user1")  # Line written by Claude
        self.assertIsInstance(result["advice_id"], str)  # Line written by Claude
        self.assertTrue(len(result["advice_id"]) > 0, "advice_id should not be empty")  # Line written by Claude
 
    def test_image_is_none_or_string(self):
        """Tests that image is either None or a valid string URL."""
        result = self.get_genai_advice("user1")  # Line written by Claude
        image = result["image"]  # Line written by Claude
        self.assertTrue(
            image is None or isinstance(image, str),  # Line written by Claude
            "Image should be None or a string URL"  # Line written by Claude
        )
 
    def test_image_not_always_populated(self):
        """Tests that image is not returned 100% of the time (run multiple calls).
 
        Per the spec, images should NOT be populated every single time.
        We run 20 calls and expect at least one None and one non-None.
        """
        images = [self.get_genai_advice("user1")["image"] for _ in range(20)]  # Line written by Claude
        has_none = any(img is None for img in images)  # Line written by Claude
        has_image = any(img is not None for img in images)  # Line written by Claude
        self.assertTrue(has_none, "Image should be None at least some of the time")  # Line written by Claude
        self.assertTrue(has_image, "Image should be populated at least some of the time")  # Line written by Claude
 
    def test_returns_different_advice_for_different_users(self):
        """Tests that calling with different user_ids returns distinct advice_ids."""
        result1 = self.get_genai_advice("user1")  # Line written by Claude
        result2 = self.get_genai_advice("user2")  # Line written by Claude
        self.assertNotEqual(
            result1["advice_id"], result2["advice_id"],  # Line written by Claude
            "Different users should get different advice_ids"  # Line written by Claude
        )
 
    def test_content_not_none(self):
        """Tests that content is never None, even on Vertex AI failure."""
        result = self.get_genai_advice("user1")  # Line written by Claude
        self.assertIsNotNone(result["content"], "Content should never be None")  # Line written by Claude
 
    @patch("data_fetcher.gen_model")
    def test_fallback_on_vertex_ai_failure(self, mock_model):
        """Tests that a fallback message is returned when Vertex AI raises an exception."""
        mock_model.generate_content.side_effect = Exception("API unavailable")  # Line written by Claude
        result = self.get_genai_advice("user1")  # Line written by Claude
        self.assertIsInstance(result["content"], str)  # Line written by Claude
        self.assertTrue(len(result["content"]) > 0, "Fallback content should not be empty")  # Line written by Claude
 
    @patch("data_fetcher.gen_model")
    def test_uses_vertex_ai_response_when_available(self, mock_model):
        """Tests that Vertex AI response text is used as the advice content."""
        mock_response = MagicMock()  # Line written by Claude
        mock_response.text = "  Great job on your run! Keep pushing!  "  # Line written by Claude
        mock_model.generate_content.return_value = mock_response  # Line written by Claude
        result = self.get_genai_advice("user1")  # Line written by Claude
        self.assertEqual(result["content"], "Great job on your run! Keep pushing!")  # Line written by Claude
 
    def test_exactly_four_keys(self):
        """Tests that the returned dict has exactly 4 keys, no more no less."""
        result = self.get_genai_advice("user1")  # Line written by Claude
        self.assertEqual(len(result), 4, "Result should have exactly 4 keys")  # Line written by Claude
 
 
if __name__ == "__main__":
    unittest.main()