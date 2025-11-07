from abc import ABC, abstractmethod
from ...schemas.events import AgentRequest

class Agent(ABC):
    @abstractmethod
    async def process(self, event: AgentRequest):
        pass

