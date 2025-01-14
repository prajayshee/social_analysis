from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import json

# This secure connect bundle is autogenerated when you download your SCB, 
# if yours is different update the file name below
cloud_config= {
  'secure_connect_bundle': r"D:\SmartMind Hackathon\env\social_analysis\python_project\secure-connect-asap.zip"
}

# This token JSON file is autogenerated when you download your token, 
# if yours is different update the file name below
with open(r"D:\SmartMind Hackathon\env\social_analysis\python_project\asap-token.json") as f:
    secrets = json.load(f)

CLIENT_ID = secrets["clientId"]
CLIENT_SECRET = secrets["secret"]

auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

rows = session.execute("SELECT * FROM keyspace1.social_media_posts LIMIT 10;")
for row in rows:
    print(row)
