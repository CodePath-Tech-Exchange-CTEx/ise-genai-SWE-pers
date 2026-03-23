#############################################################################
# data_fetcher.py
#
# This file contains functions to fetch data needed for the app.
#
# You will re-write these functions in Unit 3, and are welcome to alter the
# data returned in the meantime. We will replace this file with other data when
# testing earlier units.
#############################################################################

from datetime import datetime
from google.cloud import bigquery
import vertexai
from vertexai.generative_models import GenerativeModel
import random

# ---- Vertex AI setup ---- #
PROJECT_ID = "juan-gomez-fiu"
LOCATION = "us-central1"
vertexai.init(project=PROJECT_ID, location=LOCATION)
gen_model = GenerativeModel("gemini-2.0-flash-001")

posts = {
    "user5": {
        "username": "NateWorksOutaLot",
        "user_image": "https://i.etsystatic.com/22467704/r/il/e9acd2/2660697461/il_300x300.2660697461_h7db.jpg",
        "timestamp": "2025-05-04 07:30:00",
        "content": "Me and the boys went hiking for 2 hours up Mount Fuji the other day.\nIt was great!",
        "post_image": "https://media.istockphoto.com/id/1949006055/photo/group-of-active-hikers-walks-uphill-in-mountains.jpg?s=612x612&w=0&k=20&c=fS4V-GX6bYIKfWA6EgAt6r1osLy-YvlaAgV7wgVA2Pc=",
    }
}
users = {
    "user1": {
        "full_name": "Remi",
        "username": "remi_the_rems",
        "date_of_birth": "1990-01-01",
        "profile_image": "https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg",
        "friends": ["user2", "user3", "user4"],
    },
    "user2": {
        "full_name": "Blake",
        "username": "blake",
        "date_of_birth": "1990-01-01",
        "profile_image": "https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg",
        "friends": ["user1"],
    },
    "user3": {
        "full_name": "Jordan",
        "username": "jordanjordanjordan",
        "date_of_birth": "1990-01-01",
        "profile_image": "https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg",
        "friends": ["user1", "user4"],
    },
    "user4": {
        "full_name": "Gemmy",
        "username": "gems",
        "date_of_birth": "1990-01-01",
        "profile_image": "https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg",
        "friends": ["user1", "user3"],
    },
}


def get_user_sensor_data(user_id, workout_id):
    """Returns a list of timestampped information for a given workout.

    This function currently returns random data. You will re-write it in Unit 3.
    """
    sensor_data = []
    sensor_types = [
        "accelerometer",
        "gyroscope",
        "pressure",
        "temperature",
        "heart_rate",
    ]
    for index in range(random.randint(5, 100)):
        random_minute = str(random.randint(0, 59))
        if len(random_minute) == 1:
            random_minute = "0" + random_minute
        timestamp = "2024-01-01 00:" + random_minute + ":00"
        data = random.random() * 100
        sensor_type = random.choice(sensor_types)
        sensor_data.append(
            {"sensor_type": sensor_type, "timestamp": timestamp, "data": data}
        )
    return sensor_data


def get_user_workouts(user_id):
    """Returns a list of user's workouts.

    This function currently returns random data. You will re-write it in Unit 3.
    """
    workouts = []
    for index in range(random.randint(1, 3)):
        random_lat_lng_1 = (
            1 + random.randint(0, 100) / 100,
            4 + random.randint(0, 100) / 100,
        )
        random_lat_lng_2 = (
            1 + random.randint(0, 100) / 100,
            4 + random.randint(0, 100) / 100,
        )
        workouts.append(
            {
                "workout_id": f"workout{index}",
                "start_timestamp": "2024-01-01 00:00:00",
                "end_timestamp": "2024-01-01 00:30:00",
                "start_lat_lng": random_lat_lng_1,
                "end_lat_lng": random_lat_lng_2,
                "distance": random.randint(0, 200) / 10.0,
                "steps": random.randint(0, 20000),
                "calories_burned": random.randint(0, 100),
            }
        )
    return workouts


def get_user_profile(user_id):
    """Returns information about the given user.

    This function currently returns random data. You will re-write it in Unit 3.
    """
    if user_id not in users:
        raise ValueError(f"User {user_id} not found.")
    return users[user_id]


def get_post(user_id):
    """Fetches user info from BigQuery Users table and builds a post dict."""

    client = bigquery.Client(project="juan-gomez-fiu")

    query = """
        SELECT UserId, Username, ImageUrl
        FROM `juan-gomez-fiu.SWEpers.Users`
        WHERE UserId = @UserId
        LIMIT 1
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("UserId", "STRING", user_id)
        ]
    )

    results = client.query(query, job_config=job_config).result()

    row = None
    for r in results:
        row = r
        break

    if row is None:
        raise ValueError(f"User {user_id} not found in Users table.")

    content = random.choice(
        [
            "Had a great workout today!",
            "The AI really motivated me to push myself further, I ran 10 miles!",
            "Me and the boys went hiking for 2 hours up Mount Fuji the other day.\nIt was great!"
        ]
    )

    return {
        "user_id": row["UserId"],
        "username": row["Username"],
        "user_image": "https://i.etsystatic.com/22467704/r/il/e9acd2/2660697461/il_300x300.2660697461_h7db.jpg",
        "timestamp": "2026-03-22 12:00:00",   # hardcoded
        "content": content,  # hardcoded
        "post_image": row["ImageUrl"],  
    }

def get_user_posts(user_id):
    """Returns a list of a user's posts.

    This function currently returns random data. You will re-write it in Unit 3.
    """
    content = random.choice(
        [
            "Had a great workout today!",
            "The AI really motivated me to push myself further, I ran 10 miles!",
        ]
    )
    return [
        {
            "user_id": user_id,
            "post_id": "post1",
            "timestamp": "2024-01-01 00:00:00",
            "content": content,
            "image": "image_url",
        }
    ]


def get_genai_advice(user_id):
    """Returns the most recent advice from the GenAI model based on user data.

    Fetches the user's workout data, sends it to Gemini via Vertex AI,
    and returns personalised fitness advice. Image is not always populated.

    Input:  user_id (str)
    Output: dict with keys advice_id, timestamp, content, image
    """

    # ---- 1. Gather the user's workout context ---- #
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

    # ---- 2. Build the prompt ---- #
    prompt = f"""You are a friendly and motivating fitness coach AI.
Based on the following user workout data, give a short (2-3 sentence)
piece of personalised fitness advice. Be encouraging and specific.

Recent workouts:
{workout_summary}

Latest sensor readings:
{sensor_summary if sensor_summary else '  No sensor data available.'}

Respond with ONLY the advice text, no extra formatting."""

    # ---- 3. Call Vertex AI (Gemini) ---- #
    try:
        response = gen_model.generate_content(prompt)
        advice_content = response.text.strip()
    except Exception as e:
        print(f"[get_genai_advice] Vertex AI error: {e}")
        advice_content = (
            "Keep up the great work! Stay consistent and "
            "remember to hydrate before your next workout."
        )

    # ---- 4. Image: not populated 100% of the time ---- #
    motivational_images = [
        "https://plus.unsplash.com/premium_photo-1669048780129-051d670fa2d1?q=80&w=3870&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?q=80&w=3870&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?q=80&w=3870&auto=format&fit=crop",
    ]
    image = random.choice(motivational_images) if random.random() > 0.5 else None

    # ---- 5. Return the result ---- #
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {
        "advice_id": f'advice_{user_id}_{now.replace(" ", "_")}',
        "timestamp": now,
        "content": advice_content,
        "image": image,
    }

##############################
# SAMPLE BIGQUERY QUERY
##############################

# from google.cloud import bigquery

# client = bigquery.Client(project="juan-gomez-fiu")

# query = "SELECT * FROM `juan-gomez-fiu.SWEpers.Workouts`"
# results = client.query(query).result()

# for row in results:
#     print(dict(row))