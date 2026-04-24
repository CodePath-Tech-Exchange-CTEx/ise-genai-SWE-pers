import streamlit as st
from modules import require_user_selection
from data_fetcher import get_user_posts_from_friends, add_post, get_exercise_image
from datetime import datetime


def format_date(timestamp):
    """Formats a timestamp to mm/dd/yyyy."""
    if not timestamp:
        return ""
    try:
        return datetime.strptime(str(timestamp), "%Y-%m-%d %H:%M:%S.%f").strftime("%m/%d/%Y")
    except ValueError:
        try:
            return datetime.strptime(str(timestamp), "%Y-%m-%d %H:%M:%S").strftime("%m/%d/%Y")
        except ValueError:
            return str(timestamp)[:10]


def display_friend_post(post):
    """Displays a single friend post card."""
    username = post.get("username", post.get("author_id", "Unknown"))
    name = post.get("name", "")
    user_image = post.get("user_image", "https://placehold.co/50x50")
    post_image = post.get("image_url")

    with st.container(border=True):
        left, right = st.columns([3, 1])
        with left:
            col1, col2 = st.columns([1, 11])
            with col1:
                st.image(user_image, width=50)
            with col2:
                if name:
                    st.markdown(f"**{name}** · @{username}")
                else:
                    st.markdown(f"**@{username}**")
                st.caption(format_date(post.get("timestamp")))
            st.write(post.get("content", ""))
        with right:
            if post_image and post_image != "None":
                st.image(post_image, use_container_width=True)


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

# ---- Create Post ---- #
st.subheader("Create Post")
with st.form("create_post_form", clear_on_submit=True):
    post_content = st.text_area(
        "What's on your mind?",
        placeholder="Share your workout, progress, or just say hi...",
        max_chars=500,
    )
    submitted = st.form_submit_button("Post", type="primary", use_container_width=True)

    if submitted:
        if not post_content.strip():
            st.warning("Post can't be empty.")
        else:
            with st.spinner("Posting..."):
                image_url = get_exercise_image(post_content)
                add_post(st.session_state.current_user, post_content.strip(), image_url)
            st.success("Posted!")
            st.rerun()

st.divider()

display_friends_feed(st.session_state.current_user)