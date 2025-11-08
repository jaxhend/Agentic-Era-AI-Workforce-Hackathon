import json
from pathlib import Path
from ..services import ranker, llm_client

_FAQ_PATH = Path(__file__).resolve().parents[1] / "data" / "faq.json"

with open(_FAQ_PATH, "r", encoding="utf-8") as f:
    FAQ = json.load(f)
    QUESTIONS = [q["q"] for q in FAQ]

async def answer(question: str) -> tuple[str, str, float]:
    match_q, score = ranker.best_match(question, QUESTIONS)
    # Kui sarnasus madal, palu LLM-il vastata vabalt
    if score < 0.6:
        prompt = f"Vasta lühidalt küsimusele Eesti keeles: {question}"
        ans = await llm_client.complete(prompt, max_tokens=200)
        return ans, None, score
    # Leia valmis vastus või täienda LLM-iga
    entry = next(x for x in FAQ if x["q"] == match_q)
    base = entry.get("a", "")
    prompt = (
        "Täienda järgmist vastust, vajadusel kohanda stiili Eesti keeles.\n"
        f"Küsimus: {match_q}\nBaasvastus: {base}\nTäiendatud:"
    )
    final = await llm_client.complete(prompt, max_tokens=200)
    return final, match_q, score

