from ..services import llm_client

TEMPLATE = (
    "Koosta lühike järeltegevuse sõnum Eesti keeles (3-5 lauset) professionaalses, sõbralikus toonis.\n"
    "Sisend on vestluse kokkuvõte. Lisa selged järgmised sammud.\nKokkuvõte: {summary}\nSõnum:"
)

async def generate(summary: str) -> str:
    return await llm_client.complete(TEMPLATE.format(summary=summary), max_tokens=220)

