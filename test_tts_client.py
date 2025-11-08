import asyncio
import websockets
import uuid
import json
import aioconsole
import io
import os
import tempfile
from playsound import playsound  # cross-platform audio player

# --- Configuration ---
CLIENT_ID = uuid.uuid4()
WEBSOCKET_URI = f"ws://127.0.0.1:8000/ws/{CLIENT_ID}"
# ---

async def listen_for_audio(websocket):
    """Listens for incoming audio data, saves it to a file, and plays it."""
    print("🎧 Audio listener started. Waiting for audio from server...")
    mp3_buffer = io.BytesIO()

    try:
        while True:
            message_data = await websocket.recv()

            if isinstance(message_data, bytes):
                # Accumulate MP3 data in the buffer
                mp3_buffer.write(message_data)

            elif isinstance(message_data, str):
                message = json.loads(message_data)

                # End-of-stream signal
                if message.get("isFinal"):
                    print("End of audio stream signal received.")

                    if mp3_buffer.getbuffer().nbytes > 0:
                        print("Saving and playing audio...")
                        try:
                            # Write buffer to a temporary MP3 file
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                                tmp_file.write(mp3_buffer.getvalue())
                                temp_path = tmp_file.name

                            # Play the audio file (blocking call)
                            playsound(temp_path)

                            print("Playback finished.")
                        except Exception as e:
                            print(f"Error during audio playback: {e}")
                        finally:
                            # Cleanup
                            if os.path.exists(temp_path):
                                os.remove(temp_path)

                    # Reset buffer for next message
                    mp3_buffer = io.BytesIO()

    except websockets.exceptions.ConnectionClosed:
        print("Listener: Connection closed.")
    except Exception as e:
        print(f"An error occurred in the audio listener: {e}")


async def send_text_input(websocket):
    """Prompts for user input in the terminal and sends it to the server."""
    print("🎤 Text input sender started.")
    print("Type a sentence and press Enter to hear it spoken.")
    print("Type 'exit' or 'quit' to close the connection.\n")

    while True:
        try:
            text_to_send = await aioconsole.ainput("> ")
            if text_to_send.lower() in ["exit", "quit"]:
                break

            message = {"text": text_to_send}
            await websocket.send(json.dumps(message))
            print(f"Sent: '{text_to_send}'")

        except (KeyboardInterrupt, EOFError):
            break
        except Exception as e:
            print(f"An error occurred while sending text: {e}")
            break
    print("Text input sender finished.")


async def main():
    """Main function to connect to WebSocket and run listener/sender tasks."""
    try:
        async with websockets.connect(WEBSOCKET_URI) as websocket:
            print(f"✅ Connected to server with client ID: {CLIENT_ID}\n")

            await asyncio.gather(
                listen_for_audio(websocket),
                send_text_input(websocket)
            )

    except ConnectionRefusedError:
        print("\n---")
        print("Error: Connection refused. Please make sure the FastAPI server is running.")
        print("---\n")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        print("Cleaning up resources...")
        print("Done.")


if __name__ == "__main__":
    print("Starting TTS test client for Windows...")
    asyncio.run(main())
