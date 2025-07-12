from typing import Any, Dict, Optional

import aiohttp
from loguru import logger


class ComfyUIClient:
    def __init__(self, host: str = "localhost", port: int = 8188) -> None:
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"
        self.ws_url = f"ws://{host}:{port}/ws"
        self.session: Optional[aiohttp.ClientSession] = None
        self.websocket = None

    async def connect(self) -> bool:
        try:
            self.session = aiohttp.ClientSession()
            logger.info(f"Connecting to ComfyUI at {self.base_url}")

            response = await self.session.get(f"{self.base_url}/system_stats")
            if response.status == 200:
                logger.success("Successfully connected to ComfyUI")
                return True
            else:
                logger.error(f"Failed to connect to ComfyUI: {response.status}")
                return False

        except Exception as e:
            logger.error(f"Error connecting to ComfyUI: {e}")
            return False

    async def disconnect(self) -> None:
        if self.websocket:
            await self.websocket.close()
        if self.session:
            await self.session.close()

    async def queue_prompt(self, workflow: Dict[str, Any]) -> Optional[str]:
        if not self.session:
            logger.error("Client not connected")
            return None

        try:
            prompt_data = {"prompt": workflow, "client_id": "my-chat-ai-comfyui"}

            async with self.session.post(
                f"{self.base_url}/prompt", json=prompt_data
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    prompt_id = result.get("prompt_id")
                    logger.info(f"Queued prompt with ID: {prompt_id}")
                    return str(prompt_id) if prompt_id else None
                else:
                    logger.error(f"Failed to queue prompt: {response.status}")
                    return None

        except Exception as e:
            logger.error(f"Error queuing prompt: {e}")
            return None

    async def get_queue_status(self) -> Dict[str, Any]:
        if not self.session:
            return {"error": "Client not connected"}

        try:
            async with self.session.get(f"{self.base_url}/queue") as response:
                if response.status == 200:
                    result = await response.json()
                    return dict(result) if result else {}
                else:
                    return {"error": f"HTTP {response.status}"}
        except Exception as e:
            logger.error(f"Error getting queue status: {e}")
            return {"error": str(e)}

    async def get_history(self, prompt_id: str) -> Dict[str, Any]:
        if not self.session:
            return {"error": "Client not connected"}

        try:
            async with self.session.get(
                f"{self.base_url}/history/{prompt_id}"
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return dict(result) if result else {}
                else:
                    return {"error": f"HTTP {response.status}"}
        except Exception as e:
            logger.error(f"Error getting history: {e}")
            return {"error": str(e)}
