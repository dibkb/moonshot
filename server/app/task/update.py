from typing import Any
import json

async def send_update(queue: Any, update: str, key: str):
    update_data = {
        "type": key,
        "message": update
    }
    await queue.put(json.dumps(update_data))