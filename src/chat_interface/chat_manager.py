from typing import Any, Dict

from loguru import logger


class ChatManager:
    def __init__(self, intent_processor: Any, workflow_orchestrator: Any) -> None:
        self.intent_processor = intent_processor
        self.workflow_orchestrator = workflow_orchestrator
        self.active_sessions: Dict[str, Any] = {}

    async def start(self) -> None:
        logger.info("Starting chat manager...")

    async def process_message(
        self, user_id: str, message: str, platform: str = "default"
    ) -> Dict[str, Any]:
        try:
            logger.info(f"Processing message from {user_id} on {platform}: {message}")

            intent_result = await self.intent_processor.process(message)

            if intent_result["intent"] == "image_generation":
                workflow_result = await self.workflow_orchestrator.execute_generation(
                    intent_result["parameters"]
                )
                return {
                    "success": True,
                    "response": "Image generated successfully!",
                    "data": workflow_result,
                }

            return {
                "success": True,
                "response": (
                    "I understand your request, but I'm still learning how to "
                    "handle it."
                ),
                "data": intent_result,
            }

        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return {
                "success": False,
                "response": "Sorry, I encountered an error processing your request.",
                "error": str(e),
            }
