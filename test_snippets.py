# -*- coding: utf-8 -*-
from google.cloud import discoveryengine

project_id = 'clean-sunspot-496815-c5'
location = 'global'
data_store_id = 'ds-derecho-urbanistico_1782317718928_gcs_store'

client = discoveryengine.SearchServiceClient()
serving_config = client.serving_config_path(
    project=project_id,
    location=location,
    data_store=data_store_id,
    serving_config='default_config',
)

request = discoveryengine.SearchRequest(
    serving_config=serving_config,
    query='gestión de desechos san cristóbal',
    page_size=3,
    content_search_spec=discoveryengine.SearchRequest.ContentSearchSpec(
        snippet_spec=discoveryengine.SearchRequest.ContentSearchSpec.SnippetSpec(
            return_snippet=True
        )
    )
)

try:
    response = client.search(request)
    results = list(response.results)
    print(f"Got {len(results)} results")
    for result in results:
        print("Document:", result.document.id)
        if 'snippets' in result.document.derived_struct_data:
            for snippet in result.document.derived_struct_data['snippets']:
                print("Snippet:", snippet.get('snippet'))
except Exception as e:
    print(e)
