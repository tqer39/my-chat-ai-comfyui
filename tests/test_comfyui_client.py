import pytest
from unittest.mock import Mock, AsyncMock, patch
from src.comfyui_control import ComfyUIClient

class TestComfyUIClient:
    @pytest.fixture
    def client(self):
        return ComfyUIClient(host="localhost", port=8188)

    @pytest.mark.asyncio
    async def test_connect_success(self, client):
        with patch('aiohttp.ClientSession') as mock_session_class:
            mock_session = Mock()
            mock_response = Mock()
            mock_response.status = 200
            mock_session.get.return_value.__aenter__.return_value = mock_response
            mock_session_class.return_value = mock_session

            result = await client.connect()

            assert result is True
            assert client.session is not None

    @pytest.mark.asyncio
    async def test_connect_failure(self, client):
        with patch('aiohttp.ClientSession') as mock_session_class:
            mock_session = Mock()
            mock_response = Mock()
            mock_response.status = 500
            mock_session.get.return_value.__aenter__.return_value = mock_response
            mock_session_class.return_value = mock_session

            result = await client.connect()

            assert result is False

    @pytest.mark.asyncio
    async def test_queue_prompt_success(self, client):
        workflow = {"test": "workflow"}

        with patch('aiohttp.ClientSession') as mock_session_class:
            mock_session = Mock()
            mock_response = Mock()
            mock_response.status = 200
            mock_response.json = AsyncMock(return_value={"prompt_id": "test_id"})
            mock_session.post.return_value.__aenter__.return_value = mock_response
            mock_session_class.return_value = mock_session
            client.session = mock_session

            result = await client.queue_prompt(workflow)

            assert result == "test_id"

    @pytest.mark.asyncio
    async def test_get_queue_status(self, client):
        with patch('aiohttp.ClientSession') as mock_session_class:
            mock_session = Mock()
            mock_response = Mock()
            mock_response.status = 200
            mock_response.json = AsyncMock(return_value={"queue_running": [], "queue_pending": []})
            mock_session.get.return_value.__aenter__.return_value = mock_response
            mock_session_class.return_value = mock_session
            client.session = mock_session

            result = await client.get_queue_status()

            assert "queue_running" in result
            assert "queue_pending" in result
