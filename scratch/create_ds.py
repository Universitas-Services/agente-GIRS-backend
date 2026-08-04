from google.cloud import discoveryengine

project_id = "clean-sunspot-496815-c5"
location = "global" # Let's use global as it's the most reliable
data_store_id = "ds-derecho-urbanistico"

client = discoveryengine.DataStoreServiceClient()

# Initialize request argument(s)
data_store = discoveryengine.DataStore(
    display_name="Derecho Urbanistico",
    industry_vertical=discoveryengine.IndustryVertical.GENERIC,
    content_config=discoveryengine.DataStore.ContentConfig.CONTENT_REQUIRED,
)

request = discoveryengine.CreateDataStoreRequest(
    parent=f"projects/{project_id}/locations/{location}/collections/default_collection",
    data_store=data_store,
    data_store_id=data_store_id,
)

print(f"Creating DataStore {data_store_id}...")
try:
    operation = client.create_data_store(request=request)
    print("Waiting for operation to complete...")
    response = operation.result()
    print("DataStore created!")
    print(response)
except Exception as e:
    print(f"Error creating Datastore: {e}")
