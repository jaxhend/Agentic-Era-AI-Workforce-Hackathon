import json
import os
import uuid

from dotenv import load_dotenv
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState

from app.bus import bus
from app.core.ids import new_id
from app.schemas.events import ClientAudio, TTSAudio, ManagerAnswer, STTPartial, STTFinal, ClientSttInit, ManagerRoute, \
    AgentRequest
from app.stt.google_stt import GoogleSTT

router = APIRouter()
active_connections: dict[uuid.UUID, WebSocket] = {}
stt_instances: dict[uuid.UUID, GoogleSTT] = {}

load_dotenv()

@bus.subscribe("stt.partial")
@bus.subscribe("stt.final")
async def on_stt_result(event: STTPartial | STTFinal):
    """
    Receives an STT result event and sends it to the correct client's WebSocket.
    """
    if event.client_id in active_connections:
        websocket = active_connections[event.client_id]
        try:
            # Convert to dict and ensure UUID is serialized to string
            data = event.model_dump()
            data['client_id'] = str(data['client_id'])
            if event.is_final:
                data["role"] = "user"
            await websocket.send_json(data)
        except Exception as e:
            print(f"❌ Error sending STT result to client {event.client_id}: {e}")
    else:
        print(f"⚠️ Client {event.client_id} not in active connections")


@bus.subscribe("stt.final")
async def on_stt_final(event: STTFinal):
    await bus.publish("agent.request", AgentRequest(agent="booking", text=event.text, client_id=event.client_id))


@bus.subscribe("tts.audio")
async def on_tts_audio(event: TTSAudio):
    """
    Receives a TTS audio event and sends the audio chunk to the
    correct client's WebSocket.
    """
    if event.client_id in active_connections:
        websocket = active_connections[event.client_id]
        try:
            await websocket.send_bytes(event.chunk)
        except Exception as e:
            print(f"❌ Error sending audio to client {event.client_id}: {e}")
    else:
        print(f"Warning: Received TTS audio for disconnected client {event.client_id}")


async def _handle_websocket_message(msg: dict, client_id: uuid.UUID):
    """Handles a single WebSocket message."""
    # text frames
    if (t := msg.get("text")) is not None:
        try:
            data = json.loads(t)
        except json.JSONDecodeError:
            # ignore non-JSON text packets
            return

        if data.get("type") == "stt_init":
            await bus.publish(
                "client.stt_init",
                ClientSttInit(
                    client_id=client_id,
                    sample_rate=data.get("sampleRate", 16000),
                    encoding=data.get("encoding", "LINEAR16"),
                )
            )
        elif "text" in data and data["text"]:
            await bus.publish( # for TTS
                "manager.answer",
                ManagerAnswer(text=data["text"], trace_id=new_id("trace"), client_id=client_id)
            )

    # binary frames (audio)
    elif (b := msg.get("bytes")) is not None:
        await bus.publish("client.audio", ClientAudio(chunk=b, client_id=client_id))


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: uuid.UUID):
    await websocket.accept()
    active_connections[client_id] = websocket

    recognizer_path = (
        f"projects/{os.getenv('PROJECT_ID')}"
        f"/locations/{os.getenv('LOCATION')}"
        f"/recognizers/{os.getenv('RECOGNIZER_NAME')}"
    )
    stt = GoogleSTT(client_id=client_id, recognizer_path=recognizer_path)
    stt_instances[client_id] = stt
    await stt.start()

    try:
        while websocket.application_state == WebSocketState.CONNECTED:
            msg = await websocket.receive()
            await _handle_websocket_message(msg, client_id)

    except WebSocketDisconnect:
        print(f"🔌 Client {client_id} disconnected (WebSocketDisconnect)")
        pass
    except Exception as e:
        print(f"❌ Error in WebSocket handler for client {client_id}: {e}")
    finally:
        active_connections.pop(client_id, None)
        stt_inst = stt_instances.pop(client_id, None)
        if stt_inst:
            await stt_inst.stop()
