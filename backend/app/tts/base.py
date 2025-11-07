from abc import ABC, abstractmethod
from ..schemas.events import ManagerAnswer

class TTS(ABC):
    @abstractmethod
    async def stream(self, event: ManagerAnswer):
        pass

