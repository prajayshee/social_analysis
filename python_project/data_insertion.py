import csv
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import json
import uuid
from collections import defaultdict

# Configuration for connecting to Astra DB
cloud_config = {
    'secure_connect_bundle': r'D:\SmartMind Hackathon\env\social_analysis\python_project\secure-connect-asap.zip'  # Path to secure connect bundle
}

# Load client ID and secret from your token JSON file
with open(r"D:\SmartMind Hackathon\env\social_analysis\python_project\asap-token.json") as f:
    secrets = json.load(f)

CLIENT_ID = secrets["clientId"]
CLIENT_SECRET = secrets["secret"]

auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

# Set the keyspace
session.set_keyspace('keyspace1')  # Replace 'keyspace1' with your actual keyspace name

# Create the table if not exists
session.execute("""
    CREATE TABLE IF NOT EXISTS social_media_posts (
        post_type TEXT,
        post_id UUID,
        likes INT,
        shares INT,
        comments INT,
        PRIMARY KEY (post_type, post_id)
    );
""")

# Read and insert data from CSV file
with open(r'D:\SmartMind Hackathon\env\social_analysis\app\engagement_data.csv', mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        post_type = row['post_type']
        post_id = uuid.uuid4()  # Generate a unique UUID for each post
        likes = int(row['likes'])
        shares = int(row['shares'])
        comments = int(row['comments'])

        # Insert data into the table
        session.execute("""
            INSERT INTO social_media_posts (post_type, post_id, likes, shares, comments)
            VALUES (%s, %s, %s, %s, %s);
        """, (post_type, post_id, likes, shares, comments))

print("Data inserted successfully!")

# Query the data to calculate average engagement per post type
rows = session.execute("SELECT post_type, likes, shares, comments FROM social_media_posts;")

# Calculate averages in Python
engagement_data = defaultdict(lambda: {'likes': 0, 'shares': 0, 'comments': 0, 'count': 0})

for row in rows:
    post_type = row.post_type
    engagement_data[post_type]['likes'] += row.likes
    engagement_data[post_type]['shares'] += row.shares
    engagement_data[post_type]['comments'] += row.comments
    engagement_data[post_type]['count'] += 1

# Print average engagement per post type
for post_type, data in engagement_data.items():
    avg_likes = data['likes'] / data['count']
    avg_shares = data['shares'] / data['count']
    avg_comments = data['comments'] / data['count']
    print(f"Post Type: {post_type}")
    print(f"Average Likes: {avg_likes}")
    print(f"Average Shares: {avg_shares}")
    print(f"Average Comments: {avg_comments}")
    print()
