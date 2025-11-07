from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState

from app.bus import bus
from app.schemas.events import (
    ClientAudio,
    ManagerAnswer,
    Error,
)

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while websocket.application_state == WebSocketState.CONNECTED:
            data = await websocket.receive_bytes()
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

