from ..services import llm_client

TEMPLATE = (
    "Sa oled intenti-klassiifitseerija. Tagasta ainult üks sõna (või lühike märksõna) "
    + "kasutaja teksti põhjal. Näited: broneerimine, küsimus, kaebus, tänu, pakkumine, hinnapäring.\n\nTekst: \n{txt}\n\nIntention:"
)

async def analyze(text: str) -> str:
    prompt = TEMPLATE.format(txt=text)
    raw = await llm_client.complete(prompt, max_tokens=20)
    return raw.splitlines()[0].strip().lower()

