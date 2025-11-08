from ..services import llm_client

TEMPLATE = (
    "Sa oled Eesti keeles kirjutav copywriter. Loo {length} tekst tooniga '{tone}'. \n"
    "Sisend-brief: {brief}\n\nVäljasta ainult tekst."
)

async def generate(brief: str, tone: str = "neutraalne", length: str = "lühike") -> str:
    prompt = TEMPLATE.format(brief=brief, tone=tone, length=length)
    return await llm_client.complete(prompt, max_tokens=400)

