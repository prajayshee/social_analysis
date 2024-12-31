from astrapy import DataAPIClient

# Initialize the client
client = DataAPIClient("AstraCS:xaZFPqkWAtiGsKIuSRavEulO:aa16080e5f6fb53a7ec80f61aef527d66f2d89d4328de125a449d986ad22dc4f")
db = client.get_database_by_api_endpoint(
  "https://a1ed2a08-d406-48e0-8e31-d12ed66ab373-us-east-2.apps.astra.datastax.com"
)

print(f"Connected to Astra DB: {db.list_collection_names()}")