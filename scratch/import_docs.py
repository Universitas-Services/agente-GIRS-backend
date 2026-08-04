from google.cloud import discoveryengine

project_id = "clean-sunspot-496815-c5"
location = "global"
data_store_id = "ds-derecho-urbanistico_1782317718928_gcs_store"

client = discoveryengine.DocumentServiceClient()

# The full resource name of the search engine branch.
# e.g. projects/{project}/locations/{location}/dataStores/{data_store_id}/branches/{branch}
parent = client.branch_path(
    project=project_id,
    location=location,
    data_store=data_store_id,
    branch="default_branch",
)

gcs_uri = "gs://biblioteca-legal/tema-principal/derecho-urbanistico/legislacion/**"

request = discoveryengine.ImportDocumentsRequest(
    parent=parent,
    gcs_source=discoveryengine.GcsSource(
        input_uris=[gcs_uri], data_schema="content"
    ),
    reconciliation_mode=discoveryengine.ImportDocumentsRequest.ReconciliationMode.FULL,
)

print(f"Starting import from {gcs_uri} to DataStore {data_store_id}...")
try:
    # Make the request
    operation = client.import_documents(request=request)
    print("Waiting for operation to complete (this might take a few minutes)...")
    response = operation.result()
    print("Import completed!")
    print(response)
except Exception as e:
    print(f"Error during import: {e}")
