from rapidfuzz import process, fuzz
from typing import List, Tuple

def best_match(query: str, choices: List[str]) -> Tuple[str, float]:
    match, score, _ = process.extractOne(query, choices, scorer=fuzz.token_sort_ratio)
    return match, float(score) / 100.0

