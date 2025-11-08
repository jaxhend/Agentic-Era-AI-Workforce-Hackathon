import json
from pathlib import Path
from typing import Dict, Any
from ..core import config

_DB_PATH = Path(config.DB_URL)

def _load_db() -> Dict[str, Any]:
    if not _DB_PATH.exists():
        return {}
    with open(_DB_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def _save_db(data: Dict[str, Any]):
    with open(_DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def get_context(user_id: str) -> Dict[str, Any]:
    db = _load_db()
    return db.get(user_id, {})

def update_context(user_id: str, kv: Dict[str, Any]):
    db = _load_db()
    if user_id not in db:
        db[user_id] = {}
    for k, v in kv.items():
        db[user_id][k] = v
    _save_db(db)
