# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto se adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [Unreleased]
### Added
- Integración de convenciones de documentación del proyecto (README, CONTRIBUTING, CHANGELOG).

## [0.1.0] - 2026-07-07
### Added
- Inicialización del proyecto usando Agent Development Kit (ADK) v0.5.0.
- Lógica principal del agente (`app/agent.py`) configurada con `gemini-2.5-flash`.
- Integración RAG con Vertex AI Search (`Normativas_GIRS`).
- Despliegue configurado en GCP (Vertex AI Agent Engine).
- Pruebas unitarias e integración en el directorio `tests/`.
