from fastapi import APIRouter
from backend.app.schemas.schemas import FAQIn, FAQOut
from ..agents import faq_agent as agent

router = APIRouter(prefix="/faq", tags=["faq"])

@router.post("/answer", response_model=FAQOut)
async def answer(body: FAQIn):
    ans, mq, score = await agent.answer(body.question)
    return FAQOut(answer=ans, matched_q=mq, score=score)

