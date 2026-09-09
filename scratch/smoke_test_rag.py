"""Smoke test: verifica conectividad RAG al proyecto consultoria-girs."""
from __future__ import annotations

import os
import sys

from dotenv import load_dotenv

load_dotenv()

REQUIRED = ("GOOGLE_CLOUD_PROJECT", "ENGINE_ID")


def main() -> int:
    missing = [k for k in REQUIRED if not os.environ.get(k)]
    if missing:
        print(f"FALLO: faltan variables: {', '.join(missing)}")
        return 1

    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    engine_id = os.environ["ENGINE_ID"]
    location = os.environ.get("DISCOVERY_ENGINE_LOCATION", "global")

    print("=== Smoke test RAG GIRS ===")
    print(f"project={project_id}")
    print(f"engine={engine_id}")
    print(f"discovery_location={location}")
    print(f"compute_location={os.environ.get('GOOGLE_CLOUD_LOCATION', '(no set)')}")
    print(f"bucket={os.environ.get('LOGS_BUCKET_NAME', '(no set)')}")
    print()

    from google.api_core import client_options
    from google.cloud import discoveryengine

    api_endpoint = (
        None
        if location == "global"
        else f"{location}-discoveryengine.googleapis.com"
    )
    client_opts = client_options.ClientOptions(
        quota_project_id=project_id,
        api_endpoint=api_endpoint,
    )
    client = discoveryengine.SearchServiceClient(client_options=client_opts)
    serving_config = (
        f"projects/{project_id}/locations/{location}/collections/"
        f"default_collection/engines/{engine_id}/servingConfigs/default_config"
    )

    query = "Ley de Gestión Integral de la Basura"
    print(f"Consulta: {query}")
    print("Llamando a Vertex AI Search...")

    request = discoveryengine.SearchRequest(
        serving_config=serving_config,
        query=query,
        page_size=3,
        content_search_spec=discoveryengine.SearchRequest.ContentSearchSpec(
            snippet_spec=discoveryengine.SearchRequest.ContentSearchSpec.SnippetSpec(
                return_snippet=True
            ),
            extractive_content_spec=discoveryengine.SearchRequest.ContentSearchSpec.ExtractiveContentSpec(
                max_extractive_answer_count=1,
                max_extractive_segment_count=1,
            ),
        ),
    )

    try:
        response = client.search(request)
    except Exception as exc:
        print(f"FALLO: error al consultar Discovery Engine: {exc}")
        return 1

    results = list(response.results)
    if not results:
        print(
            "FALLO: la API respondió OK pero 0 resultados. "
            "Revisa indexación del Data Store / Engine."
        )
        return 2

    print(f"OK: {len(results)} documento(s) recuperado(s)\n")
    for i, result in enumerate(results, 1):
        doc = result.document
        data = doc.derived_struct_data or {}
        title = data.get("title") or doc.id or "(sin título)"
        snippet = ""
        if "extractive_segments" in data and data["extractive_segments"]:
            snippet = (data["extractive_segments"][0].get("content") or "")[:180]
        elif "snippets" in data and data["snippets"]:
            snippet = (data["snippets"][0].get("snippet") or "")[:180]
        print(f"{i}. {title}")
        if snippet:
            print(f"   {snippet}...")
        print()

    print("Smoke test SUPERADO: autenticación + Engine + indexación responden.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
