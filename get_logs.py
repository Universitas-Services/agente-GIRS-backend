from google.cloud import logging

client = logging.Client(project='clean-sunspot-496815-c5')
entries = client.list_entries(
    filter_='resource.type="aiplatform.googleapis.com/ReasoningEngine" AND resource.labels.reasoning_engine_id="2958970508298682368"', 
    max_results=50
)
with open('cloud_logs.txt', 'w', encoding='utf-8') as f:
    for e in entries:
        f.write(str(e.payload) + '\n')
