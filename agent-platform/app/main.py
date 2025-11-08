from fastapi import FastAPI
from .routers import (
    intent as r_intent,
    copywriter as r_copy,
    calendar_agent as r_cal,
    faq_agent as r_faq,
    analytics_agent as r_an,
    context_keeper as r_ctx,
    pricing_agent as r_price,
    sentiment_agent as r_sent,
    escalation_agent as r_esc,
    followup_agent as r_follow,
    router_agent as r_router
)

app = FastAPI(title="Agent Platform (vLLM)")

app.include_router(r_router.router) # The main entry point
app.include_router(r_intent.router)
app.include_router(r_copy.router)
app.include_router(r_cal.router)
app.include_router(r_faq.router)
app.include_router(r_an.router)
app.include_router(r_ctx.router)
app.include_router(r_price.router)
app.include_router(r_sent.router)
app.include_router(r_esc.router)
app.include_router(r_follow.router)

@app.get("/")
async def root():
    return {"ok": True, "name": "Agent Platform", "entrypoint": "/router/route", "agents": [
        "/intent", "/copywriter", "/calendar", "/faq", "/analytics",
        "/context", "/pricing", "/sentiment", "/escalate", "/followup"
    ]}

