import unittest
from unittest.mock import patch, MagicMock
import activity_page

# -----------------------------
# TESTS: get_exercise_image
# -----------------------------
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

        result = activity_page.get_exercise_image("random")

        self.assertIsNone(result)

    @patch("activity_page.requests.get")
    def test_unexpected_api_response(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {}  # missing "results"
        mock_get.return_value = mock_response

        result = activity_page.get_exercise_image("push up")

        self.assertIsNone(result)


# -----------------------------
# TESTS: add_post
# -----------------------------
class TestAddPost(unittest.TestCase):

    @patch("activity_page.client")
    @patch("activity_page.bigquery")
    def test_add_post_executes_query(self, mock_bigquery, mock_client):
        mock_query_job = MagicMock()
        mock_client.query.return_value = mock_query_job

        activity_page.add_post("user1", "test content", "http://image.com")

        mock_client.query.assert_called_once()
        mock_query_job.result.assert_called_once()


    @patch("activity_page.client")
    @patch("activity_page.bigquery")
    def test_add_post_uses_correct_parameters(self, mock_bigquery, mock_client):
        mock_query_job = MagicMock()
        mock_client.query.return_value = mock_query_job

        def fake_scalar_param(name, type_, value):
            m = MagicMock()
            m.value = value
            return m

        mock_bigquery.ScalarQueryParameter.side_effect = fake_scalar_param

        activity_page.add_post("user1", "leg day", "http://img.com")

        # Pull query_parameters from the QueryJobConfig constructor call, not the returned mock
        _, qjc_kwargs = mock_bigquery.QueryJobConfig.call_args
        params = qjc_kwargs["query_parameters"]

        self.assertEqual(params[0].value, "user1")           # author_id
        self.assertEqual(params[1].value, "http://img.com")  # image_url
        self.assertEqual(params[2].value, "leg day")         # content

    @patch("activity_page.client")
    @patch("activity_page.bigquery")
    def test_add_post_handles_none_image_url(self, mock_bigquery, mock_client):
        mock_query_job = MagicMock()
        mock_client.query.return_value = mock_query_job

        def fake_scalar_param(name, type_, value):
            m = MagicMock()
            m.value = value
            return m

        mock_bigquery.ScalarQueryParameter.side_effect = fake_scalar_param

        activity_page.add_post("user1", "test content", None)

        _, qjc_kwargs = mock_bigquery.QueryJobConfig.call_args
        params = qjc_kwargs["query_parameters"]

        self.assertEqual(params[1].value, "")


    @patch("activity_page.client")
    @patch("activity_page.bigquery")
    def test_query_contains_insert(self, mock_bigquery, mock_client):
        mock_query_job = MagicMock()
        mock_client.query.return_value = mock_query_job

        activity_page.add_post("user1", "test", "img")

        args, _ = mock_client.query.call_args
        query_string = args[0]

        self.assertIn("INSERT INTO", query_string)
        self.assertIn("Posts", query_string)


# -----------------------------
# TESTS: get_user_workouts
# -----------------------------
class TestGetUserWorkouts(unittest.TestCase):

    @patch("activity_page.client")
    def test_returns_workouts(self, mock_client):
        mock_row1 = {"WorkoutId": "w1", "UserId": "user1"}
        mock_row2 = {"WorkoutId": "w2", "UserId": "user1"}

        mock_query_job = MagicMock()
        mock_query_job.result.return_value = [mock_row1, mock_row2]

        mock_client.query.return_value = mock_query_job

        result = activity_page.get_user_workouts("user1")

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["WorkoutId"], "w1")

    @patch("activity_page.client")
    def test_returns_empty_list(self, mock_client):
        mock_query_job = MagicMock()
        mock_query_job.result.return_value = []

        mock_client.query.return_value = mock_query_job

        result = activity_page.get_user_workouts("user1")

        self.assertEqual(result, [])

    @patch("activity_page.client")
    def test_query_contains_user_id(self, mock_client):
        mock_query_job = MagicMock()
        mock_query_job.result.return_value = []

        mock_client.query.return_value = mock_query_job

        activity_page.get_user_workouts("user123")

        args, _ = mock_client.query.call_args
        query_string = args[0]

        self.assertIn("user123", query_string)


# -----------------------------
# RUN TESTS
# -----------------------------
if __name__ == "__main__":
    unittest.main()