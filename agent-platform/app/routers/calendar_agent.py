from fastapi import APIRouter
from ..models.schemas import CalendarIn, CalendarOut
from ..agents import calendar_agent as agent

router = APIRouter(prefix="/calendar", tags=["calendar"])

@router.post("/interpret", response_model=CalendarOut)
async def interpret(body: CalendarIn):
    data = await agent.interpret(body.utterance)
    return CalendarOut(**data)

