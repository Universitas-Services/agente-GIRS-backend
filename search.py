import os
from google.cloud import discoveryengine

project_id = 'agente-manual-contrataciones'
location = 'global'
data_store_id = 'derecho-urbanistico-pdfs_1782529893492_gcs_store'

client = discoveryengine.SearchServiceClient()
serving_config = client.serving_config_path(
    project=project_id,
    location=location,
    data_store=data_store_id,
    serving_config='default_config',
)

request = discoveryengine.SearchRequest(
    serving_config=serving_config,
    query='¿Cuáles son los instrumentos del control previo ambiental que establece la Ley Orgánica del Ambiente?',
    page_size=5,
    content_search_spec=discoveryengine.SearchRequest.ContentSearchSpec(
        snippet_spec=discoveryengine.SearchRequest.ContentSearchSpec.SnippetSpec(
            return_snippet=True
        ),
        extractive_content_spec=discoveryengine.SearchRequest.ContentSearchSpec.ExtractiveContentSpec(
            max_extractive_answer_count=1,
            max_extractive_segment_count=1
        )
    )
)

response = client.search(request)

print('Resultados de busqueda:')
for result in response.results:
    print(f'Document: {result.document.name}')
    if hasattr(result.document, 'derived_struct_data'):
        struct_data = result.document.derived_struct_data
        if 'extractive_segments' in struct_data:
            for segment in struct_data['extractive_segments']:
                print('Snippet:', segment.get('content'))
