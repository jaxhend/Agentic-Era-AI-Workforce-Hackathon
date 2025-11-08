from fastapi import APIRouter
from ..models.schemas import ContextGetIn, ContextUpdateIn
from ..agents import context_keeper as agent

router = APIRouter(prefix="/context", tags=["context"])

@router.post("/get")
async def get_ctx(body: ContextGetIn):
    return await agent.get(body.user_id)

@router.post("/update")
async def update_ctx(body: ContextUpdateIn):
    return await agent.update(body.user_id, body.kv)

