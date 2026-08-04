# Historial de Resolución de Errores y Configuración de Gemini

Este documento resume todos los problemas técnicos encontrados durante la configuración y despliegue del Agente Urbanístico, y las soluciones implementadas para que el entorno funcione de manera estable tanto en local como en producción.

---

## 1. Error de Dependencias en Cloud Build (Conflicto de Versiones de Python)
**Síntoma:** Al desplegar el agente, el proceso de compilación en la nube (Cloud Build) fallaba resolviendo dependencias de `google-cloud` y `grpcio` lanzando un error en la resolución del árbol de paquetes.
**Causa Raíz:** El comando `agents-cli deploy` captura la versión de Python del entorno local que ejecuta el comando. El sistema local tenía Python 3.14 instalado globalmente, lo que causaba que el contenedor de la nube intentara compilar con Python 3.14, una versión incompatible con algunas librerías pre-compiladas. Adicionalmente, el directorio `.venv` local se estaba subiendo al entorno de Cloud Build, creando conflictos binarios.
**Solución Implementada:**
- Se forzó el uso de Python 3.11 definiendo `requires-python = "==3.11.*"` en el archivo `pyproject.toml`.
- Se instaló `agents-cli` globalmente bajo un entorno estricto de Python 3.11 mediante `uv`.
- Se omitió el `.venv` local durante el despliegue para que Cloud Build descargue las dependencias nativas limpias para Linux.

## 2. Error gRPC 13 (INTERNAL) en Cloud Run
**Síntoma:** Tras desplegar en Cloud Run, las llamadas RAG a Vertex AI Search fallaban intermitentemente con un error `grpc StatusCode.INTERNAL` o `Received RST_STREAM with error code 13`.
**Causa Raíz:** Cloud Run tiene limitaciones al manejar streams gRPC de larga duración (idle connections) que utiliza nativamente la librería `google-cloud-discoveryengine`.
**Solución Implementada:**
- Se abandonó Cloud Run tradicional.
- Se migró el motor de cómputo a **Vertex AI Agent Engine (Reasoning Engine)**, el cual está diseñado específicamente para ejecutar agentes de IA de Google y maneja las conexiones gRPC y los tiempos de espera del modelo de forma nativa.

## 3. Caída Silenciosa del Contenedor en Reasoning Engine (Permission Denied)
**Síntoma:** El despliegue de `agents-cli deploy` indicaba éxito en la compilación, pero el recurso de Reasoning Engine fallaba al iniciar con el mensaje `"failed to start and cannot serve traffic"`.
**Causa Raíz:** En `app/agent.py` existía un bloque de código que usaba `google.auth.default()` para capturar dinámicamente el ID del proyecto e inyectarlo en la variable `GOOGLE_CLOUD_PROJECT`. En la nube, Agent Runtime corre dentro de un proyecto interno de Google (Tenant Project) y al capturar ese ID, el agente intentaba hacer consultas sobre la infraestructura de Google, lo que lanzaba un error `403 PermissionDenied` (Cloud Resource Manager API) cerrando el servidor al instante durante el arranque.
**Solución Implementada:**
- Se eliminó la captura dinámica del ID del proyecto en `app/agent.py`. Reasoning Engine ya inyecta automáticamente la variable `GOOGLE_CLOUD_PROJECT` correcta (`clean-sunspot-496815-c5`).
- Se habilitó la API de `cloudresourcemanager.googleapis.com` en el proyecto por seguridad adicional.

## 4. Retiro de API Keys y Transición a Vertex AI Nativo
**Síntoma:** Anteriormente se intentó usar una `GEMINI_API_KEY` generada desde AI Studio, pero causaba bloqueos de seguridad `403 Forbidden` al ser invocada desde la red en la nube, y fallaba en las regiones por restricciones de la API.
**Solución Implementada:**
- Se eliminó por completo el uso de API Keys (`GEMINI_API_KEY`).
- El proyecto utiliza **Application Default Credentials (ADC)** nativas de Google Cloud, aprovechando la Service Account automática de Reasoning Engine en producción y la identidad del desarrollador en local.
- El modelo se configuró de forma definitiva como `gemini-2.5-flash` consumiendo directamente el servicio regionalizado `us-east1` de Vertex AI.

---

## 5. Ecosistema Final del Agente
- **Framework de desarrollo:** Google ADK (Agent Development Kit).
- **Modelo LLM activo:** `gemini-2.5-flash`
- **Orquestador (Frontend conversacional):** Gemini Enterprise Agent Platform.
- **Backend y Cómputo:** Vertex AI Agent Engine (Reasoning Engine).
- **Almacén de Datos (RAG):** Vertex AI Search (Discovery Engine).
