import asyncio
import json
import websockets
import aiohttp
from typing import Dict, Any, Optional
from loguru import logger

class ComfyUIClient:
    def __init__(self, host: str = "localhost", port: int = 8188):
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"
        self.ws_url = f"ws://{host}:{port}/ws"
        self.session = None
        self.websocket = None

    async def connect(self):
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

    async def disconnect(self):
        if self.websocket:
            await self.websocket.close()
        if self.session:
            await self.session.close()

    async def queue_prompt(self, workflow: Dict[str, Any]) -> Optional[str]:
        try:
            prompt_data = {
                "prompt": workflow,
                "client_id": "my-chat-ai-comfyui"
            }

            async with self.session.post(
                f"{self.base_url}/prompt",
                json=prompt_data
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    prompt_id = result.get("prompt_id")
                    logger.info(f"Queued prompt with ID: {prompt_id}")
                    return prompt_id
                else:
                    logger.error(f"Failed to queue prompt: {response.status}")
                    return None

        except Exception as e:
            logger.error(f"Error queuing prompt: {e}")
            return None

    async def get_queue_status(self) -> Dict[str, Any]:
        try:
            async with self.session.get(f"{self.base_url}/queue") as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return {"error": f"HTTP {response.status}"}
        except Exception as e:
            logger.error(f"Error getting queue status: {e}")
            return {"error": str(e)}

    async def get_history(self, prompt_id: str) -> Dict[str, Any]:
        try:
            async with self.session.get(f"{self.base_url}/history/{prompt_id}") as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return {"error": f"HTTP {response.status}"}
        except Exception as e:
            logger.error(f"Error getting history: {e}")
            return {"error": str(e)}
