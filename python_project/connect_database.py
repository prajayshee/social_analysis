from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import json

cloud_config = {
    'secure_connect_bundle': 'D:\\SmartMind Hackathon\\env\\social_analysis\\python_project\\secure-connect-asap.zip'
}

try:
    # Read the secrets from the JSON file
    with open("D:\\SmartMind Hackathon\\env\\social_analysis\\python_project\\asap-token.json") as f:
        secrets = json.load(f)

    CLIENT_ID = secrets["clientId"]
    CLIENT_SECRET = secrets["secret"]

    auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)

    # Connect to the Astra DB instance
    session = cluster.connect()

    # Test the connection by querying the release version
    row = session.execute("select release_version from system.local").one()

    if row:
        print(row[0])
    else:
        print("An error occurred.")

except Exception as e:
    print(f"Error: {str(e)}")
