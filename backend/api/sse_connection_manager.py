import asyncio
import json
import signal
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

class SSEConnectionManager:
    """
    A generator for pushing game state updates to clients
    from https://stackoverflow.com/a/79423537
    """
    _instance = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance
        self.active_connections: list[asyncio.Queue] = []

    def __init__(self):
        loop = asyncio.get_running_loop()
        loop.add_signal_handler(signal.SIGINT, self.close)

    async def connect(self):
        queue = asyncio.Queue()
        self.active_connections.append(queue)
        while True:
            try:
                event = await queue.get()
                yield f"data: {json.dumps(event)}\n\n"
            except (asyncio.CancelledError, asyncio.QueueShutDown):
                self.active_connections.remove(queue)
                break

    async def broadcast(self, message: dict[str, Any]):
        await asyncio.gather(*(queue.put(message) for queue in self.active_connections))

    def close(self):
        for queue in self.active_connections:
            queue.shutdown()

manager = SSEConnectionManager()
