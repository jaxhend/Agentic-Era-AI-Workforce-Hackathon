from fastapi import APIRouter
from backend.app.schemas.schemas import AnalyticsIn, AnalyticsOut
from ..agents import analytics_agent as agent

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.post("/summary", response_model=AnalyticsOut)
async def summary(body: AnalyticsIn):
    out = await agent.summarize(body.events)
    return AnalyticsOut(summary=out)

