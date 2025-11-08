from datetime import datetime

def log_event(kind: str, payload):
    print(f"[{datetime.utcnow().isoformat()}] {kind}: {payload}")

