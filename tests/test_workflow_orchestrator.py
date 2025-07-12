import pytest
from unittest.mock import Mock, AsyncMock
from src.workflow_engine import WorkflowOrchestrator

class TestWorkflowOrchestrator:
    @pytest.fixture
    def mock_client(self):
        client = Mock()
        client.queue_prompt = AsyncMock(return_value="test_prompt_id")
        client.get_history = AsyncMock(return_value={
            "test_prompt_id": {
                "outputs": {"images": ["test.png"]}
            }
        })
        return client
    
    @pytest.fixture
    def orchestrator(self, mock_client):
        return WorkflowOrchestrator(mock_client)
    
    @pytest.mark.asyncio
    async def test_execute_generation_basic(self, orchestrator, mock_client):
        parameters = {
            "prompt": "a beautiful landscape",
            "nsfw_filter": False
        }
        
        result = await orchestrator.execute_generation(parameters)
        
        assert result["success"] is True
        assert result["prompt_id"] == "test_prompt_id"
        mock_client.queue_prompt.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_execute_generation_with_nsfw_filter(self, orchestrator, mock_client):
        parameters = {
            "prompt": "a portrait",
            "nsfw_filter": True
        }
        
        result = await orchestrator.execute_generation(parameters)
        
        assert result["success"] is True
        mock_client.queue_prompt.assert_called_once()
    
    def test_create_workflow_from_template_basic(self, orchestrator):
        parameters = {"prompt": "test prompt"}
        
        workflow = orchestrator._create_workflow_from_template("basic_generation", parameters)
        
        assert "1" in workflow
        assert workflow["2"]["inputs"]["text"] == "test prompt"
    
    def test_create_workflow_from_template_nsfw(self, orchestrator):
        parameters = {"prompt": "test prompt"}
        
        workflow = orchestrator._create_workflow_from_template("nsfw_filtered_generation", parameters)
        
        assert "7" in workflow
        assert "8" in workflow
        assert workflow["7"]["class_type"] == "NudenetModelLoader"
        assert workflow["8"]["class_type"] == "ApplyNudenet"
