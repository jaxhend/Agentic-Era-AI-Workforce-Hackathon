from ..bus import bus
#from ..core.config import ELEVENLABS_API_KEY
from ..schemas.events import ManagerAnswer, TTSAudio
#from elevenlabs import generate, stream
from .base import TTS


class ElevenLabsStream(TTS):
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def stream(self, event: ManagerAnswer):
        audio_stream = await generate(
            text=event.text,
            api_key=self.api_key,
            stream=True
        )
        for chunk in audio_stream:
            await bus.publish("tts.audio", TTSAudio(chunk=chunk))

#@bus.subscribe("manager.answer")
#async def on_manager_answer(event: ManagerAnswer):
    #if ELEVENLABS_API_KEY:
        #tts = ElevenLabsStream(api_key=ELEVENLABS_API_KEY)
       # await tts.stream(event)

