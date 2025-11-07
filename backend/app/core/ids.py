import shortuuid


def new_id(prefix: str) -> str:
    return f"{prefix}_{shortuuid.uuid()}"


import os

# TODO: Use Pydantic's BaseSettings for robust config
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
