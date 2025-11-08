from collections import Counter
from ..services import llm_client

async def summarize(events: list[dict]) -> str:
    # Väga lihtne kokkuvõte + LLM-i narratiiv
    types = Counter(e.get("type", "unknown") for e in events)
    intents = Counter(e.get("intent", "unknown") for e in events)
    base = (
        f"Sündmusi kokku: {len(events)}\n"
        f"Tüübid: {dict(types)}\n"
        f"Intentsid: {dict(intents)}\n"
    )
    prompt = (
        "Koosta Eesti keeles äriline kokkuvõte klientide sündmustest järgmise toorinfo põhjal. "
        "Too 3-5 põhipunkti ja 2 soovitust.\nToorinfo:\n" + base
    )
    story = await llm_client.complete(prompt, max_tokens=250)
    return story

