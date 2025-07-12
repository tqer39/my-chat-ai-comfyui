import asyncio
from typing import Any, Dict, Generator
from unittest.mock import AsyncMock, Mock

import pytest


@pytest.fixture
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_comfyui_client() -> Mock:
    client = Mock()
    client.connect = AsyncMock(return_value=True)
    client.disconnect = AsyncMock()
    client.queue_prompt = AsyncMock(return_value="test_prompt_id")
    client.get_queue_status = AsyncMock(
        return_value={"queue_running": [], "queue_pending": []}
    )
    client.get_history = AsyncMock(
        return_value={"test_prompt_id": {"outputs": {"images": ["test.png"]}}}
    )
    return client


@pytest.fixture
def sample_workflow() -> Dict[str, Any]:
    return {
        "1": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {"ckpt_name": "test_model.ckpt"},
        },
        "2": {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": "test prompt", "clip": ["1", 1]},
        },
    }
