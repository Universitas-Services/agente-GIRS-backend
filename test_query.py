# -*- coding: utf-8 -*-
import asyncio
from app.agent import root_agent
from google.adk.agents.context import Context

async def main():
    query = 'sobre ORDENANZA SOBRE GESTIÓN INTEGRAL DE DESECHOS Y RESIDUOS SÓLIDOS DEL MUNICIPIO SAN CRISTÓBAL dime el articulo 3'
    try:
        ctx = Context()
        async for event in root_agent.run(ctx=ctx, node_input=query):
            if hasattr(event, 'data') and isinstance(event.data, str):
                print(event.data, end="")
            elif hasattr(event, 'text') and event.text:
                print(event.text, end="")
    except Exception as e:
        print(f'Error input: {e}')

if __name__ == '__main__':
    asyncio.run(main())
