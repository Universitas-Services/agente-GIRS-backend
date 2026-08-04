import time
from google.cloud import discoveryengine
from google.api_core.exceptions import AlreadyExists

# Configuración
PROJECT_ID = "clean-sunspot-496815-c5"
LOCATION = "global"
# Generamos un nuevo ID único para este datastore de tipo "No estructurado"
DATA_STORE_ID = "ds-derecho-urb-pdf"
DISPLAY_NAME = "Derecho Urbanístico (PDFs)"

# URIs de GCS - Usamos /** para incluir la carpeta y todas sus subcarpetas
GCS_URIS = [
    "gs://biblioteca-legal/tema-principal/derecho-urbanistico/**"
]

def create_data_store():
    client = discoveryengine.DataStoreServiceClient()
    parent = f"projects/{PROJECT_ID}/locations/{LOCATION}/collections/default_collection"
    
    data_store = discoveryengine.DataStore(
        display_name=DISPLAY_NAME,
        industry_vertical=discoveryengine.IndustryVertical.GENERIC,
        solution_types=[discoveryengine.SolutionType.SOLUTION_TYPE_SEARCH],
        # CONTENT_REQUIRED es clave para Datastores de tipo "Datos No Estructurados" (Unstructured)
        content_config=discoveryengine.DataStore.ContentConfig.CONTENT_REQUIRED, 
    )
    
    request = discoveryengine.CreateDataStoreRequest(
        parent=parent,
        data_store=data_store,
        data_store_id=DATA_STORE_ID
    )
    
    print(f"⏳ Creando Data Store '{DATA_STORE_ID}' en {PROJECT_ID}...")
    operation = client.create_data_store(request=request)
    print("Esperando a que la operación de creación termine (puede tomar un par de minutos)...")
    response = operation.result()
    print(f"✅ Data Store creado exitosamente: {response.name}")

def import_documents():
    client = discoveryengine.DocumentServiceClient()
    parent = f"projects/{PROJECT_ID}/locations/{LOCATION}/collections/default_collection/dataStores/{DATA_STORE_ID}/branches/default_branch"
    
    request = discoveryengine.ImportDocumentsRequest(
        parent=parent,
        gcs_source=discoveryengine.GcsSource(
            input_uris=GCS_URIS,
            # 'content' indica que el formato de origen no es estructurado (útil para PDFs, txt, HTML puro, etc.)
            data_schema="content" 
        )
    )
    
    print(f"Importando documentos desde {GCS_URIS}...")
    operation = client.import_documents(request=request)
    print("Esperando a que la importacion termine (puede tomar varios minutos dependiendo del tamano de los PDFs)...")
    
    # La operacion puede tardar bastante, mostramos el ID de la operacion
    print(f"Operacion en curso: {operation.operation.name}")
    response = operation.result()
    
    print(f"Importacion finalizada.")
    print(f"Metadatos: {operation.metadata}")

if __name__ == "__main__":
    print("--- INICIANDO CREACION DE DATASTORE PARA PDFs ---")
    try:
        create_data_store()
    except AlreadyExists:
        print(f"Nota: El Data Store {DATA_STORE_ID} ya existe. Procediendo a importar documentos...")
    except Exception as e:
        if "already exists" in str(e).lower():
            print(f"Nota: El Data Store {DATA_STORE_ID} ya existe. Procediendo a importar documentos...")
        else:
            print(f"Error al crear Data Store: {e}")
            exit(1)
            
    print("Esperando 10 segundos antes de importar documentos para asegurar que el Datastore este completamente listo...")
    time.sleep(10)
    
    try:
        import_documents()
    except Exception as e:
        print(f"Error al importar documentos: {e}")
