import csv
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import json
import uuid

# Configuration for connecting to Astra DB
cloud_config = {
    'secure_connect_bundle': 'D:\\SmartMind Hackathon\\env\\social_analysis\\python_project\\secure-connect-asap.zip'  # Replace with the path to your secure connect bundle
}

# Load client ID and secret from your token JSON file
with open("D:\\SmartMind Hackathon\\env\\social_analysis\\python_project\\asap-token.json") as f:
    secrets = json.load(f)

CLIENT_ID = secrets["clientId"]
CLIENT_SECRET = secrets["secret"]

auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

# Create the table (if not already created)
session.set_keyspace('keyspace1')  # Replace with your actual keyspace name
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
with open('D:\\SmartMind Hackathon\\env\\social_analysis\\app\\engagement_data.csv', mode='r') as file:
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
rows = session.execute("""
    SELECT post_type, AVG(likes) AS avg_likes, AVG(shares) AS avg_shares, AVG(comments) AS avg_comments
    FROM social_media_posts
    GROUP BY post_type;
""")

# Print the results
for row in rows:
    print(f"Post Type: {row.post_type}")
    print(f"Average Likes: {row.avg_likes}")
    print(f"Average Shares: {row.avg_shares}")
    print(f"Average Comments: {row.avg_comments}")
    print()
