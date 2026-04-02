#############################################################################
# data_fetcher_test.py
#
# Tests for data_fetcher.py
# Covers: get_user_sensor_data, get_user_workouts, get_genai_advice,
#         get_exercise_image, get_user_posts_from_friends, get_users
#############################################################################

import unittest
from unittest.mock import Mock, patch, MagicMock
from data_fetcher import get_user_sensor_data, get_user_workouts
from datetime import datetime


class TestDataFetcher(unittest.TestCase):
    """Tests for get_user_sensor_data"""

    @patch('data_fetcher.bigquery.Client')
    def test_get_user_sensor_data(self, MockClient):
        mock_client = MockClient.return_value
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


class TestGetUserWorkouts(unittest.TestCase):
    """Tests for get_user_workouts"""

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


class TestGetExerciseImage(unittest.TestCase):
    """Tests for get_exercise_image"""

    @patch("data_fetcher.requests.get")
    def test_successful_image_fetch(self, mock_get):
        """Returns image URL when Unsplash returns results."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "results": [{"urls": {"regular": "http://image-url.com"}}]
        }
        mock_get.return_value = mock_response

        from data_fetcher import get_exercise_image
        result = get_exercise_image("push up")
        self.assertEqual(result, "http://image-url.com")

    @patch("data_fetcher.requests.get")
    def test_no_results_returns_none(self, mock_get):
        """Returns None when Unsplash returns empty results."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"results": []}
        mock_get.return_value = mock_response

        from data_fetcher import get_exercise_image
        result = get_exercise_image("random")
        self.assertIsNone(result)

    @patch("data_fetcher.requests.get")
    def test_unexpected_api_response_returns_none(self, mock_get):
        """Returns None when response is missing results key."""
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        from data_fetcher import get_exercise_image
        result = get_exercise_image("push up")
        self.assertIsNone(result)


class TestGetUsers(unittest.TestCase):
    """Tests for get_users"""

    @patch("data_fetcher.bigquery.Client")
    def test_returns_list_of_user_ids(self, MockClient):
        """Returns a list of user ID strings."""
        mock_client = MockClient.return_value
        mock_job = MagicMock()
        mock_row1 = MagicMock()
        mock_row1.UserId = "user1"
        mock_row2 = MagicMock()
        mock_row2.UserId = "user2"
        mock_job.result.return_value = [mock_row1, mock_row2]
        mock_client.query.return_value = mock_job

        from data_fetcher import get_users
        result = get_users()
        self.assertEqual(result, ["user1", "user2"])

    @patch("data_fetcher.bigquery.Client")
    def test_returns_empty_list_when_no_users(self, MockClient):
        """Returns empty list when no users exist."""
        mock_client = MockClient.return_value
        mock_job = MagicMock()
        mock_job.result.return_value = []
        mock_client.query.return_value = mock_job

        from data_fetcher import get_users
        result = get_users()
        self.assertEqual(result, [])

    @patch("data_fetcher.bigquery.Client")
    def test_returns_empty_list_on_failure(self, MockClient):
        """Returns empty list when BigQuery raises an exception."""
        MockClient.side_effect = Exception("BigQuery unavailable")

        from data_fetcher import get_users
        result = get_users()
        self.assertEqual(result, [])


class TestGetUserPostsFromFriends(unittest.TestCase):
    """Tests for get_user_posts_from_friends"""

    @patch("data_fetcher.bigquery.Client")
    def test_returns_list(self, MockClient):
        """Returns a list of posts when BigQuery succeeds."""
        mock_client = MockClient.return_value
        mock_job = MagicMock()
        mock_row = MagicMock()
        mock_row.items.return_value = [
            ("PostId", "p1"),
            ("AuthorId", "user2"),
            ("Username", "JaneDoe"),
            ("Timestamp", "2024-01-15 08:30:00"),
            ("Content", "Great workout today!"),
        ]
        mock_job.result.return_value = [mock_row]
        mock_client.query.return_value = mock_job

        from data_fetcher import get_user_posts_from_friends
        result = get_user_posts_from_friends("user1")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["username"], "JaneDoe")
        self.assertEqual(result[0]["content"], "Great workout today!")

    @patch("data_fetcher.bigquery.Client")
    def test_returns_empty_list_when_no_posts(self, MockClient):
        """Returns empty list when no posts are found."""
        mock_client = MockClient.return_value
        mock_job = MagicMock()
        mock_job.result.return_value = []
        mock_client.query.return_value = mock_job

        from data_fetcher import get_user_posts_from_friends
        result = get_user_posts_from_friends("user1")
        self.assertEqual(result, [])

    @patch("data_fetcher.bigquery.Client")
    def test_returns_empty_list_on_failure(self, MockClient):
        """Returns empty list when BigQuery raises an exception."""
        MockClient.side_effect = Exception("BigQuery unavailable")

        from data_fetcher import get_user_posts_from_friends
        result = get_user_posts_from_friends("user1")
        self.assertEqual(result, [])


class TestGetGenaiAdvice(unittest.TestCase):
    """Tests for get_genai_advice"""

    def setUp(self):
        from data_fetcher import get_genai_advice
        self.get_genai_advice = get_genai_advice
        patcher = patch("data_fetcher.bigquery.Client")
        self.mock_bq_client = patcher.start()
        self.addCleanup(patcher.stop)

    def test_returns_dict(self):
        result = self.get_genai_advice("user1")
        self.assertIsInstance(result, dict)

    def test_has_required_keys(self):
        result = self.get_genai_advice("user1")
        for key in ["advice_id", "timestamp", "content", "image"]:
            self.assertIn(key, result, f"Missing required key: {key}")

    def test_content_is_non_empty_string(self):
        result = self.get_genai_advice("user1")
        self.assertIsInstance(result["content"], str)
        self.assertTrue(len(result["content"]) > 0)

    def test_timestamp_is_valid_format(self):
        result = self.get_genai_advice("user1")
        try:
            datetime.strptime(result["timestamp"], "%Y-%m-%d %H:%M:%S")
        except ValueError:
            self.fail(f"Timestamp '{result['timestamp']}' is not in expected format")

    def test_advice_id_contains_user_id(self):
        result = self.get_genai_advice("user1")
        self.assertIn("user1", result["advice_id"])

    def test_advice_id_is_non_empty_string(self):
        result = self.get_genai_advice("user1")
        self.assertTrue(len(result["advice_id"]) > 0)

    def test_image_is_none_or_string(self):
        result = self.get_genai_advice("user1")
        self.assertTrue(result["image"] is None or isinstance(result["image"], str))

    def test_image_not_always_populated(self):
        images = [self.get_genai_advice("user1")["image"] for _ in range(20)]
        self.assertTrue(any(img is None for img in images))
        self.assertTrue(any(img is not None for img in images))

    def test_returns_different_advice_for_different_users(self):
        result1 = self.get_genai_advice("user1")
        result2 = self.get_genai_advice("user2")
        self.assertNotEqual(result1["advice_id"], result2["advice_id"])

    def test_content_not_none(self):
        result = self.get_genai_advice("user1")
        self.assertIsNotNone(result["content"])

    @patch("data_fetcher.gen_model")
    def test_fallback_on_vertex_ai_failure(self, mock_model):
        mock_model.generate_content.side_effect = Exception("API unavailable")
        result = self.get_genai_advice("user1")
        self.assertIsInstance(result["content"], str)
        self.assertTrue(len(result["content"]) > 0)

    @patch("data_fetcher.gen_model")
    def test_uses_vertex_ai_response_when_available(self, mock_model):
        mock_response = MagicMock()
        mock_response.text = "  Great job on your run! Keep pushing!  "
        mock_model.generate_content.return_value = mock_response
        result = self.get_genai_advice("user1")
        self.assertEqual(result["content"], "Great job on your run! Keep pushing!")

    def test_exactly_four_keys(self):
        result = self.get_genai_advice("user1")
        self.assertEqual(len(result), 4)


if __name__ == "__main__":
    unittest.main()