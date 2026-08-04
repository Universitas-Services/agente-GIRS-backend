# -*- coding: utf-8 -*-
from google.cloud import discoveryengine

client = discoveryengine.DataStoreServiceClient()
parent = 'projects/clean-sunspot-496815-c5/locations/global/collections/default_collection'

try:
    stores = client.list_data_stores(parent=parent)
    for ds in stores:
        print(f'DataStore: {ds.name}')
        print(f'  Display Name: {ds.display_name}')
        print(f'  Solution Types: {ds.solution_types}')
        print(f'  Content Config: {ds.content_config}')
        print()
except Exception as e:
    print(f'Error: {e}')
