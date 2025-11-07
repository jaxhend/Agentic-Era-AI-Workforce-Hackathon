from .memory_bus import MemoryEventBus

# Create a single, shared instance of the event bus.
# All parts of the application will import this instance.
bus = MemoryEventBus()

