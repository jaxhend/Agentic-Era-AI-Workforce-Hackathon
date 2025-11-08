from fastapi import APIRouter
from ..models.schemas import TextIn, SentimentOut
from ..agents import sentiment_agent as agent

router = APIRouter(prefix="/sentiment", tags=["sentiment"])

@router.post("/analyze", response_model=SentimentOut)
async def analyze(body: TextIn):
    label, conf = await agent.analyze(body.text)
    return SentimentOut(label=label, confidence=conf)

