#!/usr/bin/env python3

import asyncio
import os

from dotenv import load_dotenv
from loguru import logger

from comfyui_control import ComfyUIClient

load_dotenv()


async def main():
    logger.info("Testing ComfyUI connection...")

    host = os.getenv("COMFYUI_HOST", "localhost")
    port = int(os.getenv("COMFYUI_PORT", "8188"))

    client = ComfyUIClient(host=host, port=port)

    try:
        success = await client.connect()
        if success:
            logger.success("Connection successful!")

            queue_status = await client.get_queue_status()
            logger.info(f"Queue status: {queue_status}")
        else:
            logger.error("Connection failed!")

    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
