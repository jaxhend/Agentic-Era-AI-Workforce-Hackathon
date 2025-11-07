import asyncio
from collections import defaultdict
from typing import Callable, Any

class MemoryEventBus:
    def __init__(self):
        self.subscribers = defaultdict(list)

    def subscribe(self, topic: str):
        def decorator(callback: Callable):
            self.subscribers[topic].append(callback)
            return callback
        return decorator

    async def publish(self, topic: str, event: Any):
        for callback in self.subscribers[topic]:
            await callback(event)

