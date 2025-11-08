from fastapi import APIRouter
from backend.app.schemas.schemas import EscalateIn, EscalateOut
from ..agents import escalation_agent as agent

router = APIRouter(prefix="/escalate", tags=["escalate"])

@router.post("/check", response_model=EscalateOut)
async def check(body: EscalateIn):
    label = body.sentiment.label if body.sentiment else None
    conf = body.sentiment.confidence if body.sentiment else None
    yes, reason = await agent.should_escalate(body.message, label, conf)
    return EscalateOut(escalate=yes, reason=reason)

