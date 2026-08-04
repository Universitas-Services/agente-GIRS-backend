import os
import google.auth
from google.cloud import discoveryengine

_, project_id = google.auth.default()
client = discoveryengine.EngineServiceClient()
request = discoveryengine.ListEnginesRequest(
    parent=f"projects/{project_id}/locations/global/collections/default_collection"
)
try:
    for engine in client.list_engines(request=request):
        print(f"App Name: {engine.display_name}")
        print(f"App ID: {engine.name}")
        print("-" * 40)
except Exception as e:
    print(f"Error: {e}")
