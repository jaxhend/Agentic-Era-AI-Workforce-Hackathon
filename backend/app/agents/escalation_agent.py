from . import sentiment_agent

async def should_escalate(message: str, given_label: str | None = None, given_conf: float | None = None) -> tuple[bool, str]:
    label, conf = (given_label, given_conf) if given_label else await sentiment_agent.analyze(message)
    if label == "negatiivne" and conf >= 0.6:
        return True, "Negatiivne tonaalsus"
    if "ei tööta" in message.lower() or "tagasimakse" in message.lower():
        return True, "Sõnum sisaldab tundlikku teemat"
    return False, "Eskalatsioon ei ole vajalik"

