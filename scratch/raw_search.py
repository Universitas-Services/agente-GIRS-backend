import os
from google.cloud import discoveryengine

project_id = 'clean-sunspot-496815-c5'
location = 'global'
data_store_id = 'ds-derecho-urbanistico_1782317718928_gcs_store'

client = discoveryengine.SearchServiceClient()
serving_config = f"projects/{project_id}/locations/{location}/collections/default_collection/engines/gemini-enterprise-17817902_1781790229220/servingConfigs/default_config"

request = discoveryengine.SearchRequest(
    serving_config=serving_config,
    query='de',
    page_size=10,
)

response = client.search(request)
results = list(response.results)
print(f"Got {len(results)} results")
for result in results:
    print(f"Doc ID: {result.document.id}")
    print(f"Derived: {result.document.derived_struct_data}")
    print(f"Struct: {result.document.struct_data}")
