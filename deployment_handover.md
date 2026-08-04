# Documentación de Despliegue: Agente Urbanístico

Este documento resume el estado actual de la infraestructura, los enlaces importantes y el proceso para mantener y consumir el agente urbanístico.

---

## 1. Ecosistema de Despliegue
El agente está construido sobre **Google ADK (Agent Development Kit)** y está integrado en los siguientes ecosistemas de Google Cloud:
*   **Google Cloud Run**: Actúa como el servidor principal. Aquí se encuentra alojado el código, los contenedores de Docker y el servidor FastAPI que ejecuta la lógica del agente.
*   **Gemini Enterprise (Agent Runtime)**: Actúa como el orquestador principal. El agente de Cloud Run está "publicado" y registrado aquí utilizando el protocolo **A2A (Agent-to-Agent)**, lo que permite que la infraestructura de Google dialogue directamente con nuestro Cloud Run.

## 2. Proyecto de Google Cloud
*   **Project ID**: `clean-sunspot-496815-c5`
*   **Project Number**: `529295899189`
*   **Región del Servidor**: `us-east1`

## 3. Data Store (Base de Datos / Búsqueda)
*   **Estado actual**: **Ninguno**. 
*   **Contexto**: Acordamos que por el momento *no* se conectarían ni el `ID_PROYECTO_DATA_STORE` ni el `ID_DATA_STORE_URBANISTICO`. Esto está pendiente de implementación futura, por lo que el agente por ahora no consulta ningún origen de datos de Vertex AI Search de manera activa.

## 4. Proceso Técnico de Actualización (Despliegue de Código)
Para actualizar la lógica del agente (por ejemplo, si modificas el código en `app/agent.py` o añades un Data Store), debes seguir estos pasos desde tu terminal (estando en la raíz del proyecto):

1. **Asegúrate de que tus cambios pasen las pruebas locales.**
2. **Ejecuta el siguiente comando para desplegar la nueva versión**:
   ```bash
   agents-cli deploy --no-wait --no-confirm-project
   ```
3. **¿Tengo que volver a publicarlo en Gemini Enterprise?**
   **No.** Como el agente está registrado por A2A (vía un Agent Card que expone Cloud Run), Gemini Enterprise consultará automáticamente las capacidades más recientes de la URL base cada vez que reciba un evento. Solo basta con que la nueva revisión de Cloud Run termine de compilarse y ponerse en verde.

## 5. Enlaces Públicos y Pruebas
*   **URL de Producción (Cloud Run)**: 
    [https://agente-urbanistico-qtekgv4raq-ue.a.run.app](https://agente-urbanistico-qtekgv4raq-ue.a.run.app)
*   **Dashboard de Gemini Enterprise**: 
    [Ver Agente en la Consola de Google Cloud](https://console.cloud.google.com/gemini-enterprise/locations/global/engines/gemini-enterprise-17817902_1781790229220/overview/dashboard?project=clean-sunspot-496815-c5)

*Nota: La URL de Cloud Run por defecto responderá `404` si abres la raíz en el navegador, ya que los endpoints operativos están bajo prefijos de API (como `/run` o `/a2a/...`).*

## 6. Endpoints para un Frontend
Si vas a construir un Frontend (como una página web en React o Next.js) para consumir este agente, tienes dos arquitecturas posibles:

### Opción A: Consumo Indirecto (Vía Google Cloud / Dialogflow / Gemini) - **Recomendado**
En lugar de que tu Frontend le hable directamente a tu código, el Frontend se conecta a la API de **Vertex AI Agent Builder** (Gemini Enterprise). Google Cloud se encargará del historial de chat, la gestión de sesiones y luego se comunicará en privado con tu Cloud Run. 
*   **API a consumir**: [Vertex AI Conversations API (Sessions:detectIntent o Sessions:serverStreamingDetectIntent)](https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/projects.locations.agents.sessions/detectIntent)

### Opción B: Consumo Directo (Directo a Cloud Run)
Si prefieres construir tu propia gestión de historial y dialogar directamente con tu código alojado en Cloud Run saltándote Gemini Enterprise, usarías los endpoints generados por el ADK:
*   **POST** `https://agente-urbanistico-qtekgv4raq-ue.a.run.app/agente-urbanistico/run`
    *   **Propósito**: Enviar un *prompt* y obtener una respuesta.
    *   **Carga útil (JSON)**: `{"prompt": "Hola, tengo una duda urbana"}`.
    *   **Nota de Autenticación**: Debido a que en el paso de despliegue establecimos `--no-allow-unauthenticated` en Cloud Run, tu Frontend (o tu backend intermediario) **deberá inyectar un Token Bearer de Google Identity (OAuth2)** en los headers para que Cloud Run no bloquee la petición con un error `403 Forbidden`.
