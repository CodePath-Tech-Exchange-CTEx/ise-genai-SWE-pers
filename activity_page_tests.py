#############################################################################
# activity_page_tests.py
#
# Tests for activity_page.py
# Covers: add_post only
# Note: get_exercise_image and get_user_workouts tests live in data_fetcher_test.py
#############################################################################

import unittest
from unittest.mock import patch, MagicMock


class TestAddPost(unittest.TestCase):
    """Tests for add_post in activity_page.py"""

    @patch("pages.activity_page._get_client")
    @patch("pages.activity_page.bigquery")
    def test_add_post_executes_query(self, mock_bigquery, mock_get_client):
        """add_post should execute a BigQuery query."""
        mock_client = mock_get_client.return_value
        mock_query_job = MagicMock()
        mock_client.query.return_value = mock_query_job

        from pages.activity_page import add_post
        add_post("user1", "test content", "http://image.com")

        mock_client.query.assert_called_once()
        mock_query_job.result.assert_called_once()

    @patch("pages.activity_page._get_client")
    @patch("pages.activity_page.bigquery")
    def test_add_post_uses_correct_parameters(self, mock_bigquery, mock_get_client):
        """add_post should pass author_id, image_url, and content as query params."""
        mock_client = mock_get_client.return_value
        mock_query_job = MagicMock()
        mock_client.query.return_value = mock_query_job

        def fake_scalar_param(name, type_, value):
            m = MagicMock()
            m.value = value
            return m

        mock_bigquery.ScalarQueryParameter.side_effect = fake_scalar_param

        from pages.activity_page import add_post
        add_post("user1", "leg day", "http://img.com")

        _, qjc_kwargs = mock_bigquery.QueryJobConfig.call_args
        params = qjc_kwargs["query_parameters"]

        self.assertEqual(params[0].value, "user1")
        self.assertEqual(params[1].value, "http://img.com")
        self.assertEqual(params[2].value, "leg day")

    @patch("pages.activity_page._get_client")
    @patch("pages.activity_page.bigquery")
    def test_add_post_handles_none_image_url(self, mock_bigquery, mock_get_client):
        """add_post should convert None image_url to empty string."""
        mock_client = mock_get_client.return_value
        mock_query_job = MagicMock()
        mock_client.query.return_value = mock_query_job

        def fake_scalar_param(name, type_, value):
            m = MagicMock()
            m.value = value
            return m

        mock_bigquery.ScalarQueryParameter.side_effect = fake_scalar_param

        from pages.activity_page import add_post
        add_post("user1", "test content", None)

        _, qjc_kwargs = mock_bigquery.QueryJobConfig.call_args
        params = qjc_kwargs["query_parameters"]

        self.assertEqual(params[1].value, "")

    @patch("pages.activity_page._get_client")
    @patch("pages.activity_page.bigquery")
    def test_query_contains_insert(self, mock_bigquery, mock_get_client):
        """add_post query should be an INSERT INTO Posts statement."""
        mock_client = mock_get_client.return_value
        mock_query_job = MagicMock()
        mock_client.query.return_value = mock_query_job

        from pages.activity_page import add_post
        add_post("user1", "test", "img")

        args, _ = mock_client.query.call_args
        query_string = args[0]

        self.assertIn("INSERT INTO", query_string)
        self.assertIn("Posts", query_string)


if __name__ == "__main__":
    unittest.main()