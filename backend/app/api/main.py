from fastapi import FastAPI
from app.api.http_router import router as http_router
from app.api.ws import router as ws_router
import importlib
import pkgutil

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    """
    Dynamically imports all submodules on startup to ensure all event
    subscribers are registered with the shared event bus.
    """
    print("--- Running startup event: Discovering and importing submodules ---")
    package_name = "app"
    package = importlib.import_module(package_name)
    for _, module_name, _ in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
        try:
            print(f"Importing submodule: {module_name}")
            importlib.import_module(module_name)
        except Exception as e:
            print(f"Failed to import {module_name}: {e}")
    print("--- Submodule discovery complete ---")


app.include_router(http_router, prefix="/api")
app.include_router(ws_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState

from ..bus.memory_bus import MemoryEventBus
from ..schemas.events import (
    ClientAudio,
    ManagerAnswer,
    Error,
)

app = FastAPI()
bus = MemoryEventBus()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while websocket.application_state == WebSocketState.CONNECTED:
            data = await websocket.receive_bytes()
            # TODO: Decode client audio, validate format
            event = ClientAudio(chunk=data)
            await bus.publish("client.audio", event)

    except WebSocketDisconnect:
        print("Client disconnected")


@bus.subscribe("manager.answer")
async def on_manager_answer(event: ManagerAnswer):
    # TODO: Send to websocket
    pass


@bus.subscribe("error")
async def on_error(event: Error):
    # TODO: Send to websocket
    pass

