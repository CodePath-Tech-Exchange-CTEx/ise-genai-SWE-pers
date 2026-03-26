#############################################################################
# community_page_tests.py
#
# Tests for community_page.py
# Covers: format_date, display_friend_post, display_friends_feed
# Note: get_user_posts_from_friends lives in data_fetcher.py and is tested
#       in data_fetcher_test.py
#############################################################################

import unittest
from unittest.mock import patch, MagicMock
from streamlit.testing.v1 import AppTest


# -----------------------------
# TESTS: format_date
# -----------------------------
class TestFormatDate(unittest.TestCase):

    def setUp(self):
        from pages.community_page import format_date
        self.format_date = format_date

    def test_valid_timestamp(self):
        """Valid timestamp returns formatted date string."""
        result = self.format_date("2024-01-15 08:30:00")
        self.assertEqual(result, "January 15, 2024")

    def test_missing_timestamp_returns_empty(self):
        """None timestamp returns empty string."""
        result = self.format_date(None)
        self.assertEqual(result, "")

    def test_empty_string_returns_empty(self):
        """Empty string returns empty string."""
        result = self.format_date("")
        self.assertEqual(result, "")

    def test_badly_formatted_timestamp_returns_first_ten(self):
        """Badly formatted timestamp returns first 10 characters."""
        result = self.format_date("2024-01-15T08:30:00Z")
        self.assertEqual(result, "2024-01-15")


# -----------------------------
# TESTS: display_friends_feed
# -----------------------------
class TestDisplayFriendsFeed(unittest.TestCase):

    def test_shows_no_posts_message_when_empty(self):
        """Shows info message when no posts are returned."""
        def run_app():
            from unittest.mock import patch
            with patch("pages.community_page.get_user_posts_from_friends", return_value=[]):
                from pages.community_page import display_friends_feed
                display_friends_feed("user1")

        at = AppTest.from_function(run_app)
        at.run()
        self.assertFalse(at.exception)

    def test_renders_single_post_without_crashing(self):
        """Renders a single post card without crashing."""
        def run_app():
            from unittest.mock import patch
            mock_posts = [
                {
                    "post_id": "p1",
                    "author_id": "user2",
                    "username": "JaneDoe",
                    "timestamp": "2024-01-15 08:30:00",
                    "content": "Great workout today!",
                }
            ]
            with patch("pages.community_page.get_user_posts_from_friends", return_value=mock_posts):
                from pages.community_page import display_friends_feed
                display_friends_feed("user1")

        at = AppTest.from_function(run_app)
        at.run()
        self.assertFalse(at.exception)

    def test_renders_multiple_posts_without_crashing(self):
        """Renders multiple post cards without crashing."""
        def run_app():
            from unittest.mock import patch
            mock_posts = [
                {
                    "post_id": f"p{i}",
                    "author_id": f"user{i}",
                    "username": f"User{i}",
                    "timestamp": "2024-01-15 08:30:00",
                    "content": f"Post content {i}",
                }
                for i in range(5)
            ]
            with patch("pages.community_page.get_user_posts_from_friends", return_value=mock_posts):
                from pages.community_page import display_friends_feed
                display_friends_feed("user1")

        at = AppTest.from_function(run_app)
        at.run()
        self.assertFalse(at.exception)

    def test_renders_post_with_missing_fields(self):
        """Renders a post card without crashing when optional fields are missing."""
        def run_app():
            from unittest.mock import patch
            mock_posts = [
                {
                    "post_id": "p1",
                    # missing username, timestamp, content
                }
            ]
            with patch("pages.community_page.get_user_posts_from_friends", return_value=mock_posts):
                from pages.community_page import display_friends_feed
                display_friends_feed("user1")

        at = AppTest.from_function(run_app)
        at.run()
        self.assertFalse(at.exception)


if __name__ == "__main__":
    unittest.main()