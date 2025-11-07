from abc import ABC, abstractmethod
from ..schemas.events import ClientAudio

class STT(ABC):
    @abstractmethod
    async def transcribe(self, event: ClientAudio):
        pass

