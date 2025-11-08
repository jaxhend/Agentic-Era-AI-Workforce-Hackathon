from fastapi import APIRouter
from ..models.schemas import CopyIn, CopyOut
from ..agents import copywriter as agent

router = APIRouter(prefix="/copywriter", tags=["copywriter"])

@router.post("/generate", response_model=CopyOut)
async def generate(body: CopyIn):
    txt = await agent.generate(body.brief, body.tone, body.length)
    return CopyOut(content=txt)

