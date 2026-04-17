import streamlit as st
from modules import display_genai_advice, require_user_selection
from data_fetcher import get_genai_advice, get_user_posts_from_friends
from datetime import datetime


def render_genai_section(user_id):
    """Fetches and displays the GenAI advice component."""
    advice_data = get_genai_advice(user_id=user_id)
    timestamp = advice_data.get("timestamp", "No Date Known...")
    content = advice_data.get("content", "No Content Known...")
    image = advice_data.get("image")
    display_genai_advice(timestamp, content, image)


def format_date(timestamp):
    """Formats a timestamp to a readable date string."""
    if not timestamp:
        return ""
    try:
        return datetime.strptime(str(timestamp), "%Y-%m-%d %H:%M:%S").strftime("%B %d, %Y")
    except ValueError:
        return str(timestamp)[:10]


def display_friend_post(post):
    """Displays a single friend post card."""
    with st.container(border=True):
        col1, col2 = st.columns([1, 9])
        with col1:
            st.image("https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&s=50", width=50)
        with col2:
            st.markdown(f"**{post.get('username', post.get('author_id', 'Unknown'))}**")
            st.caption(format_date(post.get("timestamp")))
        st.write(post.get("content", ""))


def display_friends_feed(user_id):
    """Fetches and displays the friends feed for a given user."""
    st.title("Friends Feed")
    posts = get_user_posts_from_friends(user_id)
    if not posts:
        st.info("No posts from friends yet.")
    else:
        for post in posts:
            display_friend_post(post)


st.html("""
<style>
    .block-container { padding-top: 1rem !important; }
    .hero-banner {
        background-color: #1a4fd6;
        padding: 4rem 2rem 3rem 2rem;
        margin-left: calc(-50vw + 50%);
        margin-right: calc(-50vw + 50%);
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }
</style>
<div class="hero-banner">
    <h1 style="color: white !important; font-size: 2.5rem; font-weight: 700; margin: 0; padding: 0; line-height: 1;">Community Page</h1>
</div>
""")

require_user_selection()

render_genai_section(st.session_state.current_user)
display_friends_feed(st.session_state.current_user)