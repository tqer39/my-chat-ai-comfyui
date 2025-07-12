#!/usr/bin/env python3

import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

from comfyui_control import ComfyUIClient

load_dotenv()

async def test_comfyui_connection():
    logger.info("Testing ComfyUI connection...")
    
    host = os.getenv("COMFYUI_HOST", "localhost")
    port = int(os.getenv("COMFYUI_PORT", "8188"))
    
    client = ComfyUIClient(host=host, port=port)
    
    try:
        success = await client.connect()
        if success:
            logger.success(f"Successfully connected to ComfyUI at {host}:{port}")
            
            queue_status = await client.get_queue_status()
            logger.info(f"Queue status: {queue_status}")
            
            return True
        else:
            logger.error("Failed to connect to ComfyUI")
            return False
            
    except Exception as e:
        logger.error(f"Error testing ComfyUI connection: {e}")
        return False
    finally:
        await client.disconnect()

async def setup_directories():
    logger.info("Setting up directories...")
    
    directories = [
        "logs",
        "temp",
        "outputs",
        "workflows"
    ]
    
    for directory in directories:
        path = Path(directory)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            logger.success(f"Created directory: {directory}")
        else:
            logger.info(f"Directory already exists: {directory}")

def check_environment():
    logger.info("Checking environment configuration...")
    
    required_vars = [
        "COMFYUI_HOST",
        "COMFYUI_PORT"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.warning(f"Missing environment variables: {missing_vars}")
        logger.info("Please check your .env file configuration")
    else:
        logger.success("Environment configuration looks good")
    
    return len(missing_vars) == 0

async def main():
    logger.info("=== ComfyUI Setup and Configuration ===")
    
    env_ok = check_environment()
    if not env_ok:
        logger.error("Environment configuration issues detected")
        sys.exit(1)
    
    await setup_directories()
    
    connection_ok = await test_comfyui_connection()
    if not connection_ok:
        logger.error("ComfyUI connection test failed")
        logger.info("Please ensure ComfyUI is running and accessible")
        sys.exit(1)
    
    logger.success("=== Setup completed successfully ===")
    logger.info("You can now run the main application with: python src/main.py")

if __name__ == "__main__":
    asyncio.run(main())
