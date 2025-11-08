from fastapi import APIRouter
from ..models.schemas import PricingIn, PricingOut
from ..agents import pricing_agent as agent

router = APIRouter(prefix="/pricing", tags=["pricing"])

@router.post("/quote", response_model=PricingOut)
async def quote(body: PricingIn):
    return agent.quote(body)

