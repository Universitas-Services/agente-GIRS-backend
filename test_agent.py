import os
import asyncio
from app.agent import app
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

async def main():
    pregunta = "sobre ORDENANZA SOBRE GESTIÓN INTEGRAL DE DESECHOS Y RESIDUOS SÓLIDOS DEL MUNICIPIO SAN CRISTÓBAL TITULO I DISPOSICIONES GENERALES, dime ¿Cual es el articulo3?"
    print(f"Pregunta: {pregunta}")
    print("-" * 50)
    
    try:
        session_service = InMemorySessionService()
        await session_service.create_session(app_name="app", user_id="user", session_id="s1")
        runner = Runner(agent=app.root_agent, app_name="app", session_service=session_service)
        
        async for event in runner.run_async(
            user_id="user", 
            session_id="s1",
            new_message=types.Content(role="user", parts=[types.Part.from_text(text=pregunta)]),
        ):
            print(event)
            
    except Exception as e:
        print(f"Error al ejecutar: {e}")

if __name__ == "__main__":
    asyncio.run(main())
