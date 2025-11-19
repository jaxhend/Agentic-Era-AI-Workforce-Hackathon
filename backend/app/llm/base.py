from abc import ABC, abstractmethod
from app.schemas.events import AgentRequest

class Agent(ABC):
    @abstractmethod
    async def process(self, event: AgentRequest):
        pass