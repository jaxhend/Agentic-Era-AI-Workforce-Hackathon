from ..services import llm_client

TEMPLATE = (
    "Märgi alloleva teksti tonaalsus: positiivne, neutraalne või negatiivne. "
    "Kirjuta vastuseks ainult label ja hinnang protsendina JSON-is: {label, confidence}.\n\nTekst: {txt}\nJSON:"
)

async def analyze(text: str) -> tuple[str, float]:
    import json
    raw = await llm_client.complete(TEMPLATE.format(txt=text), max_tokens=60)
    raw = raw.strip().strip('`')
    try:
        data = json.loads(raw)
        return data.get("label", "neutraalne"), float(data.get("confidence", 0.7))
    except Exception:
        # Tagavaraks heuristika
        t = text.lower()
        if any(w in t for w in ["halb", "paha", "vihane", "rahulolematu", "pettunud"]):
            return "negatiivne", 0.7
        if any(w in t for w in ["tänan", "väga hea", "super", "meeldis"]):
            return "positiivne", 0.7
        return "neutraalne", 0.6

