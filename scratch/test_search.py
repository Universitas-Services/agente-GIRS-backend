from google.cloud import discoveryengine

project_id = "clean-sunspot-496815-c5"
location = "global"
data_store_id = "ds-derecho-urbanistico"

client = discoveryengine.SearchServiceClient()

# The full resource name of the search engine serving config
# e.g. projects/{project_id}/locations/{location}/dataStores/{data_store_id}/servingConfigs/{serving_config_id}
serving_config = client.serving_config_path(
    project=project_id,
    location=location,
    data_store=data_store_id,
    serving_config="default_config",
)

request = discoveryengine.SearchRequest(
    serving_config=serving_config,
    query="variables urbanas fundamentales",
    page_size=3,
)

print(f"Searching Datastore {data_store_id}...")
try:
    response = client.search(request)
    for result in response.results:
        document = result.document
        print(f"Doc ID: {document.id}")
        
        # Unstructured documents return chunks in derived_struct_data
        if "extractive_answers" in document.derived_struct_data:
            for answer in document.derived_struct_data["extractive_answers"]:
                print(f"Snippet: {answer.get('content')}")
                
        if "snippets" in document.derived_struct_data:
            for snippet in document.derived_struct_data["snippets"]:
                print(f"Snippet: {snippet.get('snippet')}")
        
        print("---")
except Exception as e:
    print(f"Error during search: {e}")
