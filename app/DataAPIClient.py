from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

def connect_to_db():
    # Path to the secure connect bundle
    secure_connect_bundle = 'D:\SmartMind Hackathon\env\social_analysis'

    # Create the auth provider
    auth_provider = PlainTextAuthProvider('your_client_id', 'your_client_secret')  # Replace with actual credentials
    cluster = Cluster(cloud={'secure_connect_bundle': secure_connect_bundle}, auth_provider=auth_provider)
    session = cluster.connect()

    # Use your keyspace
    session.set_keyspace('your_keyspace_name')  # Replace with your actual keyspace name

    print("Connected to Astra DB!")
    return session

def test_connection():
    session = connect_to_db()
    rows = session.execute('SELECT release_version FROM system.local')
    for row in rows:
        print(f'Cassandra Version: {row.release_version}')
