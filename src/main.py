#!/usr/bin/env python3

import asyncio
import os
import sys
from typing import Optional

from dotenv import load_dotenv
from loguru import logger

from chat_interface import ChatManager
from comfyui_control import ComfyUIClient
from intent_processing import IntentProcessor
from workflow_engine import WorkflowOrchestrator

load_dotenv()


def setup_logging() -> None:
    log_level = os.getenv("LOG_LEVEL", "INFO")
    logger.remove()
    logger.add(
        sys.stderr,
        level=log_level,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        ),
    )
    logger.add(
        "logs/app.log",
        rotation="10 MB",
        retention="7 days",
        level=log_level,
        format=(
            "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - "
            "{message}"
        ),
    )


class ChatAIComfyUIApp:
    def __init__(self) -> None:
        self.comfyui_client: Optional[ComfyUIClient] = None
        self.chat_manager: Optional[ChatManager] = None
        self.intent_processor: Optional[IntentProcessor] = None
        self.workflow_orchestrator: Optional[WorkflowOrchestrator] = None

    async def initialize(self) -> None:
        logger.info("Initializing Chat AI ComfyUI application...")

        comfyui_host = os.getenv("COMFYUI_HOST", "localhost")
        comfyui_port = int(os.getenv("COMFYUI_PORT", "8188"))

        self.comfyui_client = ComfyUIClient(host=comfyui_host, port=comfyui_port)
        await self.comfyui_client.connect()

        self.intent_processor = IntentProcessor()
        self.workflow_orchestrator = WorkflowOrchestrator(self.comfyui_client)
        self.chat_manager = ChatManager(
            self.intent_processor, self.workflow_orchestrator
        )

        logger.success("Application initialized successfully")

    async def run(self) -> None:
        logger.info("Starting Chat AI ComfyUI service...")

        try:
            if self.chat_manager:
                await self.chat_manager.start()
            logger.info("Chat AI service is running. Press Ctrl+C to stop.")

            while True:
                await asyncio.sleep(1)

        except KeyboardInterrupt:
            logger.info("Shutting down...")
        except Exception as e:
            logger.error(f"Application error: {e}")
        finally:
            await self.cleanup()

    async def cleanup(self) -> None:
        if self.comfyui_client:
            await self.comfyui_client.disconnect()
        logger.info("Application shutdown complete")


async def main() -> None:
    setup_logging()

    app = ChatAIComfyUIApp()
    await app.initialize()
    await app.run()


if __name__ == "__main__":
    asyncio.run(main())
