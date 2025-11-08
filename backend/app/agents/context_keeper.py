from ..services import context_store

async def get(user_id: str) -> dict:
    return context_store.get_context(user_id)

async def update(user_id: str, kv: dict):
    context_store.update_context(user_id, kv)
    return {"ok": True}

