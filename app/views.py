from django.shortcuts import render
from django.http import JsonResponse
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from django.http import HttpResponse
import json
import logging
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

# Configuration for connecting to Astra DB
cloud_config = {
    'secure_connect_bundle': r"D:\SmartMind Hackathon\env\social_analysis\python_project\secure-connect-asap.zip"
}

# Load secrets for Astra DB connection
with open(r"D:\SmartMind Hackathon\env\social_analysis\python_project\asap-token.json") as f:
    secrets = json.load(f)

CLIENT_ID = secrets["clientId"]
CLIENT_SECRET = secrets["secret"]

auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()
session.set_keyspace('keyspace1')  # Replace with your keyspace name

# Function to get average engagement
logger = logging.getLogger(__name__)

def get_avg_engagement(request):
    try:
        # Execute the query to get average engagement data
        rows = session.execute("""
            SELECT post_type, AVG(likes) AS avg_likes, AVG(shares) AS avg_shares, AVG(comments) AS avg_comments
            FROM social_media_posts
            GROUP BY post_type;
        """)

        # Process query results into a list of dictionaries
        results = []
        for row in rows:
            results.append({
                'post_type': row.post_type,
                'avg_likes': row.avg_likes,
                'avg_shares': row.avg_shares,
                'avg_comments': row.avg_comments,
            })

        # If no data is found, return a message indicating no data available
        if not results:
            return render(request, 'avg_engagement.html', {'message': 'No data available for average engagement.'})

        # Pass the data to the template and render the page
        return render(request, 'avg_engagement.html', {'data': results})

    except Exception as e:
        # Log the exception details for debugging purposes
        logger.error(f"Error occurred while fetching average engagement data: {str(e)}", exc_info=True)

        # Render an error message to the template
        return render(request, 'avg_engagement.html', {'error': 'An error occurred while processing the request. Please try again later.'})

# Function to get posts by type
def get_cassandra_session():
    try:
        cluster = Cluster(['127.0.0.1'])  # Adjust your Cassandra node IP here
        session = cluster.connect('social_media_keyspace')  # Replace with your keyspace
        return session
    except Exception as e:
        # Handle connection errors (if any)
        print(f"Connection error: {str(e)}")
        return None  # Return None if unable to connect

def get_posts_by_type(request, post_type):
    session = get_cassandra_session()  # Get the Cassandra session

    if not session:
        # If session creation fails, return a message to the user
        return render(request, 'base.html', {'error_message': "Failed to connect to Cassandra."})

    try:
        # Query to get posts by the provided post_type (with ALLOW FILTERING)
        query = SimpleStatement("""
            SELECT * FROM social_media_posts WHERE post_type=%s ALLOW FILTERING;
        """)

        # Execute the query
        rows = session.execute(query, [post_type])

        # Prepare the posts data to be displayed
        posts = [
            {
                'post_type': row.post_type,
                'likes': row.likes,
                'shares': row.shares,
                'comments': row.comments,
                'created_at': row.created_at,  # Include creation date or other fields as needed
            }
            for row in rows
        ]
        
        # Pass the posts to the template for rendering
        return render(request, 'posts_by_type.html', {
            'posts': posts,
            'post_type': post_type
        })

    except Exception as e:
        # General error handling if something unexpected happens
        print(f"Error occurred while fetching posts: {str(e)}")
        return render(request, 'base.html', {'error_message': "An error occurred while fetching posts."})
    
# Function to list all posts
def list_all_posts(request):
    try:
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
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Function to render average engagement page
def avg_engagement(request):
    try:
        # Directly get the data from the database (no need to make external requests)
        rows = session.execute("""
            SELECT post_type, AVG(likes) AS avg_likes, AVG(shares) AS avg_shares, AVG(comments) AS avg_comments
            FROM social_media_posts
            GROUP BY post_type;
        """)
        data = [
            {
                'post_type': row.post_type,
                'avg_likes': row.avg_likes,
                'avg_shares': row.avg_shares,
                'avg_comments': row.avg_comments,
            }
            for row in rows
        ]
        return render(request, 'avg_engagement.html', {'data': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Function to render posts by type page
def posts_by_type(request, post_type):
    try:
        # Fetch posts based on post type
        rows = session.execute("""
            SELECT * FROM social_media_posts WHERE post_type=%s ALLOW FILTERING;
        """, [post_type])
        posts = [
            {
                'post_type': row.post_type,
                'likes': row.likes,
                'shares': row.shares,
                'comments': row.comments,
            }
            for row in rows
        ]
        return render(request, 'posts_by_type.html', {'posts': posts})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Base view function (can be used for testing base.html rendering)
def base(request):
    return render(request, 'base.html')
