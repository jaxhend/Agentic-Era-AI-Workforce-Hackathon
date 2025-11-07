from app.bus import bus
from app.schemas.events import AgentRequest, AgentResult
from .base import Agent


class FAQAgent(Agent):
    async def process(self, event: AgentRequest):
        # TODO: Implement FAQ logic
        result = {"answer": "This is a frequently asked question."}
        await bus.publish("agent.result", AgentResult(agent="faq", result=result, confidence=0.95))

@bus.subscribe("agent.request")
async def on_agent_request(event: AgentRequest):
    if event.agent == "faq":
        agent = FAQAgent()
        await agent.process(event)

