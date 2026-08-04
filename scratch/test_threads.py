import asyncio, threading, time
from app.agent import app
from google.adk.runners import InMemoryRunner
from google.genai import types

runner = InMemoryRunner(app=app)

def run_agent(msg):
    async def _run():
        session = await runner.session_service.create_session()
        async for event in runner.run_async("user1", session.id, types.Content(role="user", parts=[types.Part.from_text(msg)])):
            if event.output: print(f"{msg} -> {event.output}")
    try:
        asyncio.run(_run())
    except Exception as e:
        print(f"Error in {msg}: {repr(e)}")

t1 = threading.Thread(target=run_agent, args=("Msg1",))
t2 = threading.Thread(target=run_agent, args=("Msg2",))
t1.start()
time.sleep(2)
t2.start()
t1.join()
t2.join()
