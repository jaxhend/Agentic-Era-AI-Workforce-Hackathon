from ..services import llm_client

TEMPLATE = (
    "Parsi kasutaja lause sündmuse käsuks. Väljasta JSON: {action, when, title, location}.\n"
    "Action on üks: add, update, delete, query. Kui pole selge, vali add.\n\nLause: {utt}\nJSON:"
)

async def interpret(utterance: str) -> dict:
    prompt = TEMPLATE.format(utt=utterance)
    raw = await llm_client.complete(prompt, max_tokens=150)
    # Väike sanitiseerimine – kui mudel lisab koodi plokkide märke
    raw = raw.strip().strip('`')
    try:
        import json
        return json.loads(raw)
    except Exception:
        return {"action": "add", "when": None, "title": utterance[:50], "location": None}

