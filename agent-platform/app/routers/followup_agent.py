from fastapi import APIRouter
from ..models.schemas import FollowupIn, FollowupOut
from ..agents import followup_agent as agent

router = APIRouter(prefix="/followup", tags=["followup"])

@router.post("/generate", response_model=FollowupOut)
async def generate(body: FollowupIn):
    msg = await agent.generate(body.conversation_summary)
    return FollowupOut(message=msg)

