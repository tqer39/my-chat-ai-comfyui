import pytest

from src.intent_processing import IntentProcessor


class TestIntentProcessor:
    @pytest.fixture
    def processor(self) -> IntentProcessor:
        return IntentProcessor()

    @pytest.mark.asyncio
    async def test_process_image_generation_intent(
        self, processor: IntentProcessor
    ) -> None:
        message = "Generate a red sports car"

        result = await processor.process(message)

        assert result["intent"] == "image_generation"
        assert "red sports car" in result["parameters"]["prompt"]
        assert result["confidence"] > 0.5

    @pytest.mark.asyncio
    async def test_process_modification_intent(
        self, processor: IntentProcessor
    ) -> None:
        message = "Modify the image to be more colorful"

        result = await processor.process(message)

        assert result["intent"] == "image_modification"
        assert result["parameters"]["modification_type"] == "color_adjustment"

    def test_extract_style_artistic(self, processor: IntentProcessor) -> None:
        message = "create an artistic painting of a landscape"

        style = processor._extract_style(message)

        assert style == "artistic"

    def test_extract_style_realistic(self, processor: IntentProcessor) -> None:
        message = "generate a realistic photo of a person"

        style = processor._extract_style(message)

        assert style == "realistic"

    def test_should_apply_nsfw_filter(self, processor: IntentProcessor) -> None:
        message = "create a safe for work image"

        should_filter = processor._should_apply_nsfw_filter(message)

        assert should_filter is True

    def test_should_not_apply_nsfw_filter(self, processor: IntentProcessor) -> None:
        message = "create an image"

        should_filter = processor._should_apply_nsfw_filter(message)

        assert should_filter is False
