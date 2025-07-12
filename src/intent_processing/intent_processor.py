import re
from typing import Dict, Any, List
from loguru import logger

class IntentProcessor:
    def __init__(self):
        self.intent_patterns = {
            "image_generation": [
                r"generate.*image",
                r"create.*picture",
                r"make.*photo",
                r"draw.*",
                r"paint.*",
                r"render.*"
            ],
            "image_modification": [
                r"modify.*image",
                r"change.*picture",
                r"edit.*photo",
                r"adjust.*",
                r"alter.*"
            ],
            "nsfw_filter": [
                r"safe.*work",
                r"filter.*nsfw",
                r"censor.*",
                r"family.*friendly"
            ]
        }

    async def process(self, message: str) -> Dict[str, Any]:
        message_lower = message.lower()

        intent = self._classify_intent(message_lower)
        parameters = self._extract_parameters(message_lower, intent)

        return {
            "intent": intent,
            "parameters": parameters,
            "original_message": message,
            "confidence": 0.8
        }

    def _classify_intent(self, message: str) -> str:
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, message):
                    logger.info(f"Classified intent as: {intent}")
                    return intent

        logger.info("No specific intent classified, defaulting to general")
        return "general"

    def _extract_parameters(self, message: str, intent: str) -> Dict[str, Any]:
        parameters = {}

        if intent == "image_generation":
            parameters["prompt"] = self._extract_prompt(message)
            parameters["style"] = self._extract_style(message)
            parameters["nsfw_filter"] = self._should_apply_nsfw_filter(message)

        elif intent == "image_modification":
            parameters["modification_type"] = self._extract_modification_type(message)
            parameters["prompt"] = self._extract_prompt(message)

        return parameters

    def _extract_prompt(self, message: str) -> str:
        prompt_indicators = ["of", "with", "showing", "featuring"]

        for indicator in prompt_indicators:
            if indicator in message:
                parts = message.split(indicator, 1)
                if len(parts) > 1:
                    return parts[1].strip()

        return message.strip()

    def _extract_style(self, message: str) -> str:
        style_keywords = {
            "artistic": ["artistic", "art", "painting"],
            "realistic": ["realistic", "photo", "photograph"],
            "anime": ["anime", "manga", "cartoon"],
            "abstract": ["abstract", "surreal"]
        }

        for style, keywords in style_keywords.items():
            for keyword in keywords:
                if keyword in message:
                    return style

        return "default"

    def _should_apply_nsfw_filter(self, message: str) -> bool:
        safe_indicators = ["safe", "work", "family", "clean", "appropriate"]
        return any(indicator in message for indicator in safe_indicators)

    def _extract_modification_type(self, message: str) -> str:
        if "color" in message or "colour" in message:
            return "color_adjustment"
        elif "bright" in message or "dark" in message:
            return "brightness_adjustment"
        elif "background" in message:
            return "background_change"
        else:
            return "general_modification"
