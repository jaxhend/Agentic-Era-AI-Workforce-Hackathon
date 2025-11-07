from app.bus import bus
from app.schemas.events import AgentRequest, AgentResult
from .base import Agent


class BookingAgent(Agent):
    async def process(self, event: AgentRequest):
        # TODO: Implement booking logic
        result = {"status": "booked", "details": "..."}
        await bus.publish("agent.result", AgentResult(agent="booking", result=result, confidence=0.9))

@bus.subscribe("agent.request")
async def on_agent_request(event: AgentRequest):
    if event.agent == "booking":
        agent = BookingAgent()
        await agent.process(event)

