from django.shortcuts import render
import requests
from django.http import JsonResponse
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import json

# Configuration for connecting to Astra DB
cloud_config = {
    'secure_connect_bundle': r"D:\SmartMind Hackathon\env\social_analysis\python_project\secure-connect-asap.zip"
}


with open(r"D:\SmartMind Hackathon\env\social_analysis\python_project\asap-token.json") as f:
    secrets = json.load(f)

CLIENT_ID = secrets["clientId"]
CLIENT_SECRET = secrets["secret"]

auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()
session.set_keyspace('keyspace1')  # Update with your keyspace name

# Function to get average engagement
def get_avg_engagement(request):
    # Query for average engagement
    rows = session.execute("""
        SELECT post_type, AVG(likes) AS avg_likes, AVG(shares) AS avg_shares, AVG(comments) AS avg_comments
        FROM social_media_posts
        GROUP BY post_type;
    """)

    # Format the results into a dictionary
    results = []
    for row in rows:
        results.append({
            'post_type': row.post_type,
            'avg_likes': row.avg_likes,
            'avg_shares': row.avg_shares,
            'avg_comments': row.avg_comments,
        })

    # Return the results as a JSON response
    return JsonResponse(results, safe=False)

# Function to get posts by type
def get_posts_by_type(request, post_type):
    rows = session.execute("""
        SELECT * FROM social_media_posts WHERE post_type=%s ALLOW FILTERING;
    """, [post_type])
    results = [
        {
            'post_type': row.post_type,
            'likes': row.likes,
            'shares': row.shares,
            'comments': row.comments,
        }
        for row in rows
    ]
    return JsonResponse(results, safe=False)

# Function to list all posts
def list_all_posts(request):
    rows = session.execute("SELECT * FROM social_media_posts")
    posts = []
    for row in rows:
        posts.append({
            'post_type': row.post_type,
            'post_id': str(row.post_id),
            'likes': row.likes,
            'shares': row.shares,
            'comments': row.comments,
        })
    return JsonResponse(posts, safe=False)

def avg_engagement(request):
    # Call the backend API
    response = requests.get('http://127.0.0.1:8000/avg-engagement/')
    data = response.json()

    # Pass the data to the template
    return render(request, 'avg_engagement.html', {'data': data})

def posts_by_type(request, post_type):
    # Call the API for posts by type
    response = requests.get(f'http://127.0.0.1:8000/posts/{post_type}/')
    posts = response.json()

    # Render the template with the data
    return render(request, 'posts_by_type.html', {'posts': posts})
