import unittest
from unittest.mock import patch, MagicMock
import activity_page


class TestGetExerciseImage(unittest.TestCase):

    @patch("activity_page.requests.get")
    def test_successful_image_fetch(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "results": [
                {"urls": {"regular": "http://image-url.com"}}
            ]
        }
        mock_get.return_value = mock_response

        result = activity_page.get_exercise_image("push up")

        self.assertEqual(result, "http://image-url.com")
        mock_get.assert_called_once()


    @patch("activity_page.requests.get")
    def test_no_results_returns_none(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"results": []}
        mock_get.return_value = mock_response

        result = activity_page.get_exercise_image("unknown")

        self.assertIsNone(result)


    @patch("activity_page.requests.get")
    def test_api_returns_unexpected_format(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {}  # no 'results'
        mock_get.return_value = mock_response

        result = activity_page.get_exercise_image("push up")

        self.assertIsNone(result)



class TestAddPost(unittest.TestCase):

    @patch("activity_page.client")
    def test_add_post_executes_query(self, mock_client):
        mock_query_job = MagicMock()
        mock_client.query.return_value = mock_query_job

        activity_page.add_post("user1", "test content", "http://image.com")

        mock_client.query.assert_called_once()
        mock_query_job.result.assert_called_once()


    @patch("activity_page.client")
    def test_query_contains_correct_values(self, mock_client):
        mock_query_job = MagicMock()
        mock_client.query.return_value = mock_query_job

        activity_page.add_post("user1", "leg day", "http://img.com")

        args, _ = mock_client.query.call_args
        query_string = args[0]

        self.assertIn("user1", query_string)
        self.assertIn("leg day", query_string)
        self.assertIn("http://img.com", query_string)


    @patch("activity_page.client")
    def test_empty_content_still_runs_query(self, mock_client):
        mock_query_job = MagicMock()
        mock_client.query.return_value = mock_query_job

        activity_page.add_post("user1", "", "http://img.com")

        mock_client.query.assert_called_once()



class TestGetUserWorkouts(unittest.TestCase):

    @patch("activity_page.client")
    def test_returns_workouts_list(self, mock_client):
        mock_row1 = {"WorkoutId": "w1", "UserId": "user1"}
        mock_row2 = {"WorkoutId": "w2", "UserId": "user1"}

        mock_query_job = MagicMock()
        mock_query_job.result.return_value = [mock_row1, mock_row2]

        mock_client.query.return_value = mock_query_job

        result = activity_page.get_user_workouts("user1")

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["WorkoutId"], "w1")


    @patch("activity_page.client")
    def test_returns_empty_list_when_no_workouts(self, mock_client):
        mock_query_job = MagicMock()
        mock_query_job.result.return_value = []

        mock_client.query.return_value = mock_query_job

        result = activity_page.get_user_workouts("user1")

        self.assertEqual(result, [])


    @patch("activity_page.client")
    def test_query_contains_user_id(self, mock_client):
        mock_query_job = MagicMock()
        mock_client.query.return_value = mock_query_job
        mock_query_job.result.return_value = []

        activity_page.get_user_workouts("user123")

        args, _ = mock_client.query.call_args
        query_string = args[0]

        self.assertIn("user123", query_string)