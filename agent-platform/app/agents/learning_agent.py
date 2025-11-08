from ..services import context_store

# Väga lihtne: loe/uuenda promtide edu/ebaedu loendurid.
KEY = "prompt_stats"

async def record_feedback(user_id: str, ok: bool):
    ctx = context_store.get_context(user_id)
    import json
    stats = json.loads(ctx.get(KEY, "{}")) if ctx.get(KEY) else {}
    stats["ok"] = stats.get("ok", 0) + (1 if ok else 0)
    stats["nok"] = stats.get("nok", 0) + (0 if ok else 1)
    context_store.update_context(user_id, {KEY: json.dumps(stats)})
    return stats

