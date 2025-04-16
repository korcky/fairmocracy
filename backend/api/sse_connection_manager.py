import asyncio
import json
import signal
from typing import Any

class SSEConnectionManager:
    """
    A generator for pushing game state updates to clients
    from https://stackoverflow.com/a/79423537
    """
    _instance = None

    def __new__(class_, *args, **kwargs):
        if class_._instance is None:
            class_._instance = super().__new__(class_)
            class_._instance.active_connections: list[asyncio.Queue] = []  # type: ignore
        return class_._instance

    def __init__(self):
        try:
            loop = asyncio.get_running_loop()
            try:
                loop.add_signal_handler(signal.SIGINT, self.close)
            except NotImplementedError:
                pass
        except RuntimeError:
            pass

    async def connect(self):
        queue = asyncio.Queue()
        self.active_connections.append(queue)
        try:
            while True:
                event = await queue.get()
                print("Broadcasting event to client:", event)  # Debug log here
                yield f"data: {json.dumps(event)}\n\n"
        except asyncio.CancelledError:
            if queue in self.active_connections:
                self.active_connections.remove(queue)
            raise
        finally:
            if queue in self.active_connections:
                self.active_connections.remove(queue)

    async def broadcast(self, message: dict[str, Any]):
        await asyncio.gather(*(queue.put(message) for queue in self.active_connections))

    def close(self):
        self.active_connections.clear()

manager = SSEConnectionManager()
