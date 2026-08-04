# Agente GIRS

## Título y Descripción
El **Agente GIRS** es un asistente virtual diseñado para buscar y procesar información legal, ordenanzas y normativas sobre Gestión Integral de Residuos y Desechos Sólidos (GIRS). Resuelve el problema de la fragmentación y complejidad en la búsqueda de leyes y normas, consultando una biblioteca matriz (Data Store) alojada en Google Cloud Platform (GCP).

Está construido sobre la arquitectura de Google Agent Development Kit (ADK), utilizando Vertex AI Search para la recuperación de información (RAG) y los modelos de la familia Gemini 2.5.

## Ecosistema y Despliegue (Gateway Multicanal)
Este repositorio contiene **únicamente la lógica del agente y su conexión con la base de datos** (El Cerebro). El agente se despliega de forma segura y privada en *Vertex AI Reasoning Engine*.

Para interactuar con el agente a través de interfaces públicas (como Telegram, Web o WhatsApp), debes utilizar el proyecto asociado llamado **[Gateway Multicanal] gateway-ai-girs**. Dicho Gateway actúa como intermediario (BFF), recibiendo los mensajes de los usuarios, gestionando las sesiones y enviándolos de manera autenticada a este Agente Backend.

## Prerrequisitos
Para ejecutar y contribuir en este proyecto, necesitas:
- **Python 3.11** (requerido estrictamente por dependencias en la nube).
- **[uv](https://docs.astral.sh/uv/)**: Gestor de paquetes de Python ultrarrápido.
- **[Google Cloud CLI](https://cloud.google.com/sdk/docs/install)**: Herramienta de línea de comandos para autenticación con GCP.
- **agents-cli**: CLI oficial para la gestión de agentes (`uv tool install google-agents-cli`).

## Instalación y Configuración

Sigue estos pasos para levantar el entorno en tu máquina local:

1. **Clonar el repositorio y entrar al directorio:**
   ```bash
   git clone <url-del-repo>
   cd Agente-GIRS
   ```

2. **Instalar el CLI de agentes y sus dependencias:**
   ```bash
   uvx google-agents-cli setup
   agents-cli install
   ```

3. **Autenticación con Google Cloud (Application Default Credentials):**
   El sistema no usa API Keys. Debes iniciar sesión con tu cuenta de GCP que tenga los permisos necesarios sobre el proyecto.
   ```bash
   gcloud auth application-default login
   gcloud config set project <tu-id-de-proyecto>
   ```

## Scripts Principales

A continuación se listan los comandos más utilizados para operar el proyecto:

- **Levantar el servidor local (Desarrollo):**
  ```bash
  agents-cli playground
  ```
- **Ejecutar pruebas (Unitarias e Integración):**
  ```bash
  uv run pytest tests/unit tests/integration
  ```
- **Revisión de calidad de código (Linting):**
  ```bash
  agents-cli lint
  ```
- **Despliegue a Producción (GCP Reasoning Engine):**
  *Nota: Antes de desplegar, asegúrate de renombrar o excluir la carpeta `.venv` si estás en Windows.*
  ```bash
  agents-cli deploy
  ```
