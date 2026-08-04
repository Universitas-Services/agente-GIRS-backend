import os
from google.cloud import discoveryengine

def inspect_documents():
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
    
    request = discoveryengine.ListDocumentsRequest(parent=parent)
    docs = list(client.list_documents(request=request))
    
    for i, doc in enumerate(docs):
        print(f"--- Document {i+1} ---")
        print(f"ID: {doc.id}")
        print(f"Name: {doc.name}")
        
        # Check what fields are actually populated in the document
        has_content = doc.content is not None and len(doc.content.raw_bytes) > 0
        print(f"Has raw_bytes: {has_content}")
        
        if doc.content and doc.content.mime_type:
            print(f"MIME Type: {doc.content.mime_type}")
            
        if doc.content and doc.content.uri:
            print(f"URI: {doc.content.uri}")
            
        print(f"Struct Data: {doc.struct_data}")
        print(f"Index Status: {doc.index_status}")
        
        # Check if the document has unstructured content extraction data available
        # It's usually not returned in ListDocuments, so we might need a GetDocument request
        # but the view here should tell us if it's GCS linked.
        
    # Let's do a GetDocument for the first one to see full details
    if docs:
        print("\n--- Detailed GetDocument for the first doc ---")
        doc_request = discoveryengine.GetDocumentRequest(name=docs[0].name)
        full_doc = client.get_document(request=doc_request)
        print(f"Full doc struct_data: {full_doc.struct_data}")
        if full_doc.content:
            print(f"Full doc URI: {full_doc.content.uri}")
            print(f"Full doc MIME: {full_doc.content.mime_type}")

if __name__ == '__main__':
    inspect_documents()
