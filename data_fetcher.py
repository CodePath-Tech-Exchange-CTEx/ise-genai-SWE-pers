#############################################################################
# data_fetcher.py
#
# This file contains functions to fetch data needed for the app.
#############################################################################

from datetime import datetime
from google.cloud import bigquery
import vertexai
from vertexai.generative_models import GenerativeModel
import random
import requests

# ---- BigQuery client ---- #
def _get_client():
    return bigquery.Client(project="juan-gomez-fiu")

# ---- Vertex AI setup ---- #
PROJECT_ID = "juan-gomez-fiu"
LOCATION = "us-central1"
vertexai.init(project=PROJECT_ID, location=LOCATION)
gen_model = GenerativeModel("gemini-2.0-flash-001")


# ---- Used by: leaderboard_page.py ---- #
def get_user_total_stats():
    """Returns a table that contains the sums of different metrics for all users"""
    query = """SELECT 
    u.UserId,
    
    SUM(w.TotalSteps) AS GrandTotalSteps,
    SUM(w.TotalDistance) AS GrandTotalDistance,
    SUM(w.CaloriesBurned) AS GrandTotalCalories
    FROM 
        `juan-gomez-fiu.SWEpers.Workouts` AS w
    JOIN 
        `juan-gomez-fiu.SWEpers.Users` AS u 
        ON w.UserId = u.UserId
    GROUP BY 
        u.UserId
    ORDER BY 
        GrandTotalCalories DESC;"""
    #conert reults to dict
    results = _get_client().query(query).result()
    results = [dict(row.items()) for row in results]
    return results
    

# ---- Used by: community_page.py ---- #
def get_user_posts_from_friends(user_id):
    """Returns the 10 most recent posts from a user's friends."""
    query = """
        SELECT p.PostId, p.AuthorId, p.Timestamp, p.Content,
               u.Username
        FROM `juan-gomez-fiu.SWEpers.Posts` p
        JOIN `juan-gomez-fiu.SWEpers.Friends` f
            ON (p.AuthorId = f.UserId2 AND f.UserId1 = @user_id)
            OR (p.AuthorId = f.UserId1 AND f.UserId2 = @user_id)
        JOIN `juan-gomez-fiu.SWEpers.Users` u
            ON p.AuthorId = u.UserId
        ORDER BY p.Timestamp DESC
        LIMIT 10
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("user_id", "STRING", user_id)
        ]
    )
    try:
        results = _get_client().query(query, job_config=job_config).result()
        posts = []
        for row in results:
            row_dict = dict(row.items())
            posts.append({
                "post_id": row_dict.get("PostId", ""),
                "author_id": row_dict.get("AuthorId", ""),
                "username": row_dict.get("Username", "Unknown"),
                "timestamp": str(row_dict.get("Timestamp", "")),
                "content": row_dict.get("Content", ""),
            })
        return posts
    except Exception as e:
        print(f"[get_user_posts_from_friends] Error: {e}")
        return []


# ---- Used by: activity_page.py, community_page.py ---- #
def get_users():
    """Returns a list of all user IDs."""
    try:
        query = "SELECT UserId FROM `juan-gomez-fiu`.SWEpers.Users"
        results = _get_client().query(query).result()
        return [row.UserId for row in results]
    except Exception as e:
        print(f"[get_users] Error: {e}")
        return []


# ---- Used by: activity_page.py ---- #
def get_exercise_image(post_text):
    """Returns an exercise image URL from Unsplash based on post text."""
    import os
    ACCESS_KEY = os.environ.get("ACCESS_KEY")
    url = "https://api.unsplash.com/search/photos"
    headers = {"Authorization": f"Client-ID {ACCESS_KEY}"}
    params = {"query": f"{post_text} exercise gym", "per_page": 1}
    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        if data.get("results"):
            return data["results"][0]["urls"]["regular"]
    except Exception as e:
        print(f"[get_exercise_image] Error: {e}")
    return None


# ---- Used by: app.py, modules_test.py ---- #
def get_user_workouts(user_id):
    """Returns a list of user's workouts. Some data in a workout may not be populated."""
    workouts = []
    query = f"""SELECT 
    * FROM 
    `juan-gomez-fiu`.SWEpers.Workouts
WHERE 
    UserId = @user_id
ORDER BY 
    EndTimestamp DESC
"""
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("user_id", "STRING", user_id)
        ]
    )
    try:
        query_job = _get_client().query(query, job_config=job_config)
        for row in query_job.result():
            row_dict = dict(row.items())
            start_lat = row_dict.get("StartLocationLat")
            start_lng = row_dict.get("StartLocationLong")
            end_lat = row_dict.get("EndLocationLat")
            end_lng = row_dict.get("EndLocationLong")
            workouts.append({
                "workout_id": row_dict.get("WorkoutId"),
                "start_timestamp": str(row_dict.get("StartTimestamp")) if row_dict.get("StartTimestamp") else None,
                "end_timestamp": str(row_dict.get("EndTimestamp")) if row_dict.get("EndTimestamp") else None,
                "start_lat_lng": (start_lat, start_lng) if start_lat is not None and start_lng is not None else None,
                "end_lat_lng": (end_lat, end_lng) if end_lat is not None and end_lng is not None else None,
                "distance": row_dict.get("TotalDistance"),
                "steps": row_dict.get("TotalSteps"),
                "calories_burned": row_dict.get("CaloriesBurned"),
            })
    except Exception as e:
        print(f"[get_user_workouts] Error: {e}")
    return workouts


# ---- Used by: activity_log_page.py ---- #
def add_workout(user_id, start_timestamp, end_timestamp, distance, steps, calories):
    """Inserts a new workout into BigQuery."""
    query = """
    INSERT INTO `juan-gomez-fiu`.SWEpers.Workouts
    (WorkoutId, UserId, StartTimestamp, EndTimestamp, TotalDistance, TotalSteps, CaloriesBurned)
    VALUES (
      GENERATE_UUID(),
      @user_id,
      @start_timestamp,
      @end_timestamp,
      @distance,
      @steps,
      @calories
    )
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
            bigquery.ScalarQueryParameter("start_timestamp", "DATETIME", start_timestamp),
            bigquery.ScalarQueryParameter("end_timestamp", "DATETIME", end_timestamp),
            bigquery.ScalarQueryParameter("distance", "FLOAT64", float(distance)),
            bigquery.ScalarQueryParameter("steps", "INT64", int(steps)),
            bigquery.ScalarQueryParameter("calories", "FLOAT64", float(calories)),
        ]
    )
    try:
        _get_client().query(query, job_config=job_config).result()
    except Exception as e:
        print(f"[add_workout] BigQuery Error: {e}")
        raise e


# ---- Used by: data_fetcher_test.py ---- #
def get_user_sensor_data(user_id, workout_id):
    """Returns sensor data for a given workout."""
    query = f"""
        SELECT t1.Timestamp, t2.Name AS SensorName, t1.SensorValue, t2.Units
        FROM `juan-gomez-fiu`.SWEpers.SensorData AS t1
        JOIN `juan-gomez-fiu`.SWEpers.SensorTypes AS t2
        ON t1.SensorId = t2.SensorId
        WHERE t1.WorkoutID = '{workout_id}'
    """
    try:
        results = _get_client().query(query).result()
        return [
            {"sensor_type": row.SensorName, "timestamp": row.Timestamp,
             "data": row.SensorValue, "units": row.Units}
            for row in results
        ]
    except Exception as e:
        print(f"[get_user_sensor_data] Error: {e}")
        return []


# ---- Used by: app.py ---- #
def get_user_profile(user_id):
    """Returns information about the given user."""
    query = """
        SELECT UserId, Name, Username, ImageUrl, DateOfBirth
        FROM `juan-gomez-fiu.SWEpers.Users`
        WHERE UserId = @user_id
        LIMIT 1
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("user_id", "STRING", user_id)
        ]
    )
    try:
        results = _get_client().query(query, job_config=job_config).result()
        row = next(iter(results), None)
        if row is None:
            raise ValueError(f"User {user_id} not found in Users table.")
        return {
            "name": row["Name"],
            "username": row["Username"],
            "user_image": row["ImageUrl"],
            "date_of_birth": str(row["DateOfBirth"]),
        }
    except Exception as e:
        print(f"[get_user_profile] Error: {e}")
        return {}


# ---- Used by: app.py ---- #
def get_post(user_id):
    """Returns the most recent post for a user."""
    query = """
        SELECT PostId, AuthorId, Timestamp, ImageUrl, Content
        FROM `juan-gomez-fiu.SWEpers.Posts`
        WHERE AuthorId = @user_id
        ORDER BY Timestamp DESC
        LIMIT 1
    """
    query2 = """
        SELECT Username, ImageUrl
        FROM `juan-gomez-fiu.SWEpers.Users`
        WHERE UserId = @user_id
        LIMIT 1
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("user_id", "STRING", user_id)
        ]
    )
    try:
        results = _get_client().query(query, job_config=job_config).result()
        results2 = _get_client().query(query2, job_config=job_config).result()
        row = next(iter(results), None)
        row2 = next(iter(results2), None)
        if row is None or row2 is None:
            raise ValueError(f"No posts found for user {user_id}.")
        return {
            "username": row2["Username"],
            "user_image": row2["ImageUrl"] or "https://placehold.co/50x50",
            "timestamp": row["Timestamp"],
            "content": row["Content"],
            "image_url": row["ImageUrl"],
        }
    except Exception as e:
        print(f"[get_post] Error: {e}")
        return {
            "username": "Unknown",
            "user_image": "https://placehold.co/50x50",
            "timestamp": "N/A",
            "content": "No post available.",
            "image_url": None,
        }


# ---- Used by: pages/home.py ---- #
def get_latest_post():
    """Returns the most recent post from any user."""
    query = """
        SELECT p.PostId, p.AuthorId, p.Timestamp, p.ImageUrl, p.Content,
               u.Username, u.ImageUrl AS UserImage
        FROM `juan-gomez-fiu.SWEpers.Posts` p
        JOIN `juan-gomez-fiu.SWEpers.Users` u ON p.AuthorId = u.UserId
        ORDER BY p.Timestamp DESC
        LIMIT 1
    """
    try:
        results = _get_client().query(query).result()
        row = next(iter(results), None)
        if row is None:
            raise ValueError("No posts found.")
        return {
            "username": row["Username"],
            "user_image": row["UserImage"] or "https://placehold.co/50x50",
            "timestamp": row["Timestamp"],
            "content": row["Content"],
            "image_url": row["ImageUrl"],
        }
    except Exception as e:
        print(f"[get_latest_post] Error: {e}")
        return {
            "username": "Unknown",
            "user_image": "https://placehold.co/50x50",
            "timestamp": "N/A",
            "content": "No post available.",
            "image_url": None,
        }


# ---- Used by: app.py ---- #
def get_user_posts(user_id):
    """Returns a list of a user's posts."""
    query = """
        SELECT PostId, AuthorId, Timestamp, ImageUrl, Content
        FROM `juan-gomez-fiu.SWEpers.Posts`
        WHERE AuthorId = @user_id
        ORDER BY Timestamp DESC
        LIMIT 3
    """
    query2 = """
        SELECT Username, ImageUrl
        FROM `juan-gomez-fiu.SWEpers.Users`
        WHERE UserId = @user_id
        LIMIT 1
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("user_id", "STRING", user_id)
        ]
    )
    try:
        results = _get_client().query(query, job_config=job_config).result()
        results2 = _get_client().query(query2, job_config=job_config).result()
        row2 = next(iter(results2), None)
        if row2 is None:
            raise ValueError(f"User {user_id} not found.")
        posts = []
        for row in results:
            posts.append({
                "username": row2["Username"],
                "user_image": row2["ImageUrl"],
                "timestamp": row["Timestamp"],
                "content": row["Content"],
                "image_url": row["ImageUrl"],
            })
        if not posts:
            raise ValueError(f"No posts found for user {user_id}.")
        return posts
    except Exception as e:
        print(f"[get_user_posts] Error: {e}")
        return []


# ---- Used by: app.py, community_page.py ---- #
def get_genai_advice(user_id):
    """Returns personalised fitness advice from Gemini based on user workout data."""
    workouts = get_user_workouts(user_id)
    sensor_summary = ""

    if workouts:
        latest = workouts[0]
        sensor_data = get_user_sensor_data(user_id, latest["workout_id"])
        if sensor_data:
            sensor_summary = "\n".join(
                f"  - {s['sensor_type']}: {s['data']:.1f} at {s['timestamp']}"
                for s in sensor_data[:10]
            )
        workout_summary = "\n".join(
            f"  - {w['distance']} km, {w['steps']} steps, "
            f"{w['calories_burned']} cal ({w['start_timestamp']} to {w['end_timestamp']})"
            for w in workouts
        )
    else:
        workout_summary = "  No workouts recorded yet."

    prompt = f"""You are a friendly and motivating fitness coach AI.
Based on the following user workout data, give a short (2-3 sentence)
piece of personalised fitness advice. Be encouraging and specific.

Recent workouts:
{workout_summary}

Latest sensor readings:
{sensor_summary if sensor_summary else '  No sensor data available.'}

Respond with ONLY the advice text, no extra formatting."""

    try:
        response = gen_model.generate_content(prompt)
        advice_content = response.text.strip()
    except Exception as e:
        print(f"[get_genai_advice] Vertex AI error: {e}")
        advice_content = (
            "Keep up the great work! Stay consistent and "
            "remember to hydrate before your next workout."
        )

    motivational_images = [
        "https://plus.unsplash.com/premium_photo-1669048780129-051d670fa2d1?q=80&w=3870&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?q=80&w=3870&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?q=80&w=3870&auto=format&fit=crop",
    ]
    image = random.choice(motivational_images) if random.random() > 0.5 else None

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {
        "advice_id": f'advice_{user_id}_{now.replace(" ", "_")}',
        "timestamp": now,
        "content": advice_content,
        "image": image,
    }