from django.shortcuts import render
from django.http import JsonResponse
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import json
import logging
from django.urls import reverse

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
session.set_keyspace('keyspace1')

logger = logging.getLogger(__name__)

def get_avg_engagement(request):
    try:
        rows = session.execute("""
            SELECT post_type, AVG(likes) AS avg_likes, AVG(shares) AS avg_shares, AVG(comments) AS avg_comments
            FROM social_media_posts
            GROUP BY post_type ALLOW FILTERING;
        """)
        data = [
            {'post_type': row.post_type, 'avg_likes': row.avg_likes, 'avg_shares': row.avg_shares, 'avg_comments': row.avg_comments}
            for row in rows
        ]
        if not data:
            return render(request, 'avg_engagement.html', {'message': 'No data available for average engagement.'})
        return render(request, 'avg_engagement.html', {'data': data})
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        return render(request, 'avg_engagement.html', {'error': 'An error occurred. Please try again later.'})

def get_posts_by_type(request, post_type):
    try:
        # Fetch posts from Cassandra by post_type
        rows = session.execute("""
            SELECT post_type, likes, shares, comments
            FROM social_media_posts
            WHERE post_type = %s;
        """, [post_type])

        if not rows:
            return render(request, 'posts_by_type.html', {'post_type': post_type, 'message': f"No posts found for type: {post_type}"})

        # Convert rows into a list of posts
        posts = [
            {
                'post_type': row.post_type,
                'likes': row.likes,
                'shares': row.shares,
                'comments': row.comments,
            }
            for row in rows
        ]

        # Return the appropriate template with data
        return render(request, 'posts_by_type.html', {'post_type': post_type, 'posts': posts})

    except Exception as e:
        logger.error(f"Error fetching posts by type {post_type}: {str(e)}", exc_info=True)
        return render(request, 'posts_by_type.html', {'post_type': post_type, 'error': 'An error occurred while fetching the posts. Please try again later.'})

def list_all_posts(request):
    try:
        rows = session.execute("SELECT * FROM social_media_posts")
        posts = [
            {'post_type': row.post_type, 'post_id': str(row.post_id), 'likes': row.likes, 'shares': row.shares, 'comments': row.comments}
            for row in rows
        ]
        return JsonResponse(posts, safe=False)
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        return JsonResponse({'error': 'An error occurred. Please try again later.'}, status=500)

def base(request):
    posts_url = reverse('get_posts_by_type', kwargs={'post_type': 'example_type'})
    return render(request, 'base.html', {'posts_url': posts_url})

def search_posts_by_type(request):
    post_type = request.GET.get('post_type')  # Retrieve the post type from the search form
    posts = []
    error = None

    if post_type:
        try:
            rows = session.execute("""
                SELECT post_type, likes, shares, comments
                FROM social_media_posts
                WHERE post_type = %s;
            """, [post_type])

            # Check if rows were fetched
            if rows:
                posts = [
                    {
                        'post_type': row.post_type,
                        'likes': row.likes,
                        'shares': row.shares,
                        'comments': row.comments,
                    }
                    for row in rows
                ]
            else:
                error = f"No posts found for type: {post_type}"

        except Exception as e:
            logger.error(f"Error searching posts by type {post_type}: {str(e)}", exc_info=True)
            error = 'An error occurred while searching for posts. Please try again later.'

    return render(request, 'base.html', {'post_type': post_type, 'posts': posts, 'error': error})