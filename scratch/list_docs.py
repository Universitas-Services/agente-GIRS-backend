import os
from google.cloud import discoveryengine

def list_documents():
    project_id = 'clean-sunspot-496815-c5'
    location = 'global'
    data_store_id = 'ds-derecho-urbanistico_1782317718928_gcs_store'

    client = discoveryengine.DocumentServiceClient()
    parent = client.branch_path(
        project=project_id,
        location=location,
        data_store=data_store_id,
        branch='default_branch'
    )
    
    print(f"Listando documentos en {parent}")
    try:
        request = discoveryengine.ListDocumentsRequest(parent=parent)
        docs = list(client.list_documents(request=request))
        print(f"Total documentos: {len(docs)}")
        for i, doc in enumerate(docs[:5]):
            print(f"Doc {i+1}: {doc.id} - {doc.struct_data.get('title', 'No title') if doc.struct_data else 'No struct_data'}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    list_documents()
