from typing import Any

async def send_update(queue: Any, update: str):
    await queue.put(update)