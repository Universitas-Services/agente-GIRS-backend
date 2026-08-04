# -*- coding: utf-8 -*-
from google.cloud import discoveryengine

client = discoveryengine.EngineServiceClient()
parent = 'projects/clean-sunspot-496815-c5/locations/global/collections/default_collection'

try:
    engines = client.list_engines(parent=parent)
    for engine in engines:
        print(f'Engine: {engine.name}')
        print(f'  Display Name: {engine.display_name}')
        print(f'  Solution Type: {engine.solution_type}')
        print(f'  Data Store IDs: {engine.data_store_ids}')
        print()
except Exception as e:
    print(f'Error: {e}')
