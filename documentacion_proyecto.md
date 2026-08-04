# Documentación del Proyecto: Agente Urbanístico

Este documento resume el progreso, la arquitectura y las resoluciones de problemas clave del proyecto "Agente Urbanístico" hasta la fecha.

## 1. Descripción General del Proyecto

El **Agente Urbanístico** es un asistente virtual diseñado para buscar y procesar información legal, ordenanzas y normativas urbanísticas consultando una biblioteca matriz (Data Store) alojada en Google Cloud Platform (GCP).
Está construido utilizando el **Agent Development Kit (ADK)** y se conecta nativamente a los servicios de **Vertex AI** y **Gemini Enterprise**.

## 2. Arquitectura de Despliegue

El despliegue está diseñado bajo una arquitectura sin servidor altamente optimizada en Google Cloud Platform:
- **Plataforma de Cómputo:** Vertex AI Agent Engine (Reasoning Engine).
- **Región:** `us-east1`.
- **Registro del Agente:** Agente A2A (App-to-App) publicable en Gemini Enterprise.
- **Modelos de IA:** `gemini-2.5-flash` mediante Vertex AI nativo (Sin API Keys).
- **Recuperación de Datos (RAG):** Integración con Vertex AI Search (Discovery Engine) en GCP para consultas normativas mediante la herramienta RAG integrada (`consulta_normativa_urbanistica`).

## 3. Configuración y Autenticación

El sistema funciona con **Application Default Credentials (ADC)** nativas. No se utilizan API Keys de AI Studio bajo ninguna circunstancia.

### Entorno Local (Desarrollo)
Para probar localmente, se utiliza el CLI oficial de agentes y el entorno virtual (`uv`):
```bash
agents-cli playground
```
El código detectará automáticamente tu inicio de sesión activo de Google Cloud CLI (`gcloud auth application-default login`) y usará la red de Google Cloud asumiendo tu identidad de usuario y los permisos que ésta posea.

### Entorno de Producción (Agent Runtime)
En la nube, el agente corre dentro de **Reasoning Engine**, el cual asume automáticamente la identidad de una Service Account dedicada (`service-529295899189@gcp-sa-aiplatform-re.iam.gserviceaccount.com`).
Esta Service Account tiene permisos automáticos y privilegios heredados para interactuar tanto con el modelo Gemini como con el buscador de Discovery Engine dentro de los límites del proyecto.

## 4. Flujo de Trabajo de Despliegue (Actualización de Código)

Cuando realices modificaciones en el código local (por ejemplo, actualizando `app/agent.py` o añadiendo nuevas herramientas), debes seguir este procedimiento exacto para subir la nueva versión a la nube y evitar errores de compilación:

### Pasos para Desplegar Cambios a Producción:

1. **Prueba local:** Asegúrate de que el agente funciona en tu máquina ejecutando `agents-cli playground`.
2. **Prepara el entorno (Paso Crítico):** Dado que estás desarrollando en Windows, subir el entorno virtual (`.venv`) precompilado causará fallos en los servidores Linux de Google. **Debes renombrar o excluir tu carpeta `.venv`** temporalmente (por ejemplo, renómbrala a `.venv_oculto` o asegúrate de que `.gitignore` / `.dockerignore` la estén bloqueando correctamente en la subida).
3. **Ejecuta el despliegue:** En la raíz del proyecto, ejecuta el comando oficial:
   ```bash
   agents-cli deploy --no-wait --no-confirm-project --project clean-sunspot-496815-c5
   ```
4. **Monitorea el estado:** El comando anterior dispara el despliegue en segundo plano. Para saber cuándo ha terminado y el servidor está listo, ejecuta:
   ```bash
   agents-cli deploy --status
   ```
   *(Espera a que este comando devuelva un mensaje de "Deployment successful!").*

**Sobre la compilación en la nube:**
Para asegurar que las dependencias compilen correctamente en la nube y evitar fallos por discrepancia de arquitecturas, el archivo `pyproject.toml` fuerza estáticamente el uso de **Python 3.11** (`requires-python = "==3.11.*"`). Esto evita conflictos con librerías precompiladas como `grpcio` al construir el entorno Linux en Cloud Build.
## 5. Próximos Pasos Recomendados

El agente ya se encuentra operando de forma 100% estable bajo el motor Agent Engine. Los próximos pasos recomendados para la evolución del proyecto son:
1. **Publicar en Gemini Enterprise:** Al generar un nuevo despliegue (cambios en código), si se desea sincronizar de inmediato la interfaz de usuario corporativa de Gemini Enterprise (el portal `.vertexaisearch.cloud.google.com`), ejecutar el comando interactivo: `agents-cli publish gemini-enterprise --interactive`.
2. **Monitoreo Avanzado:** El código cuenta con soporte para OpenTelemetry preconfigurado por `agents-cli`. Se pueden consultar los registros detallados de interacciones y tiempos de respuesta en el Log Explorer de GCP filtrando por el recurso `Reasoning Engine`.
3. **Expansión del Datastore:** Alimentar con más documentos (PDFs, ordenanzas, leyes de expropiación, etc.) el Datastore existente para potenciar las respuestas generativas de la herramienta RAG.
