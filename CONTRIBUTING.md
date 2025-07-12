# Contributing Guide

Thank you for your interest in contributing to my-chat-ai-comfyui! This guide will help you get started with
contributing to the project.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [Contributing Process](#contributing-process)
5. [Code Style and Standards](#code-style-and-standards)
6. [Testing Requirements](#testing-requirements)
7. [Documentation](#documentation)
8. [Pull Request Process](#pull-request-process)
9. [Issue Reporting](#issue-reporting)
10. [Community](#community)

## Code of Conduct

This project adheres to a code of conduct that we expect all contributors to follow. Please read and follow our
[Code of Conduct](CODE_OF_CONDUCT.md) to help us maintain a welcoming and inclusive community.

### Our Standards

- **Be respectful**: Treat everyone with respect and kindness
- **Be inclusive**: Welcome newcomers and help them get started
- **Be collaborative**: Work together to solve problems and improve the project
- **Be constructive**: Provide helpful feedback and suggestions

## Getting Started

### Prerequisites

Before contributing, make sure you have:

- Python 3.8 or higher
- Git for version control
- ComfyUI installation (for testing)
- Basic understanding of AI/ML concepts
- Familiarity with chat AI systems

### Areas for Contribution

We welcome contributions in the following areas:

- **Core Features**: Chat AI integration, workflow orchestration, NSFW filtering
- **Documentation**: Guides, tutorials, API documentation
- **Testing**: Unit tests, integration tests, performance tests
- **Bug Fixes**: Identifying and fixing issues
- **Performance**: Optimization and efficiency improvements
- **Platform Support**: Additional chat platforms, deployment options
- **Examples**: Sample applications and use cases

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/my-chat-ai-comfyui.git
cd my-chat-ai-comfyui

# Add the original repository as upstream
git remote add upstream https://github.com/tqer39/my-chat-ai-comfyui.git
```

### 2. Set Up Development Environment

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### 3. Configure Environment

```bash
# Copy example configuration
cp config/example.env .env

# Edit .env with your development settings
# Make sure to set up ComfyUI connection details
```

### 4. Verify Setup

```bash
# Run tests to verify everything is working
python -m pytest tests/

# Start the development server
python src/main.py
```

## Contributing Process

### 1. Choose an Issue

- Look for issues labeled `good first issue` for beginners
- Check issues labeled `help wanted` for areas needing assistance
- Create a new issue if you want to work on something not already tracked

### 2. Create a Branch

```bash
# Update your main branch
git checkout main
git pull upstream main

# Create a feature branch
git checkout -b feature/your-feature-name
```

### 3. Make Changes

- Write clean, well-documented code
- Follow the existing code style and patterns
- Add tests for new functionality
- Update documentation as needed

### 4. Test Your Changes

```bash
# Run the full test suite
python -m pytest tests/

# Run linting and formatting checks
black src/ tests/
flake8 src/ tests/
mypy src/

# Test with ComfyUI integration
python tests/integration/test_comfyui_integration.py
```

### 5. Commit and Push

```bash
# Stage your changes
git add .

# Commit with a descriptive message
git commit -m "feat: add natural language processing for image styles"

# Push to your fork
git push origin feature/your-feature-name
```

## Code Style and Standards

### Python Code Style

We follow PEP 8 with some modifications:

- **Line length**: 88 characters (Black default)
- **Imports**: Use absolute imports, group by standard library, third-party, local
- **Type hints**: Required for all public functions and methods
- **Docstrings**: Google-style docstrings for all public functions

### Example Code Style

```python
from typing import Dict, Any, Optional
from loguru import logger

class IntentProcessor:
    """Processes natural language intents for ComfyUI operations.

    This class handles the analysis of user messages to extract
    actionable intents and parameters for image generation.

    Attributes:
        intent_patterns: Dictionary mapping intent types to regex patterns.
    """

    def __init__(self) -> None:
        """Initialize the intent processor with default patterns."""
        self.intent_patterns = self._load_default_patterns()

    async def process(self, message: str) -> Dict[str, Any]:
        """Process a natural language message to extract intent.

        Args:
            message: The user's natural language input.

        Returns:
            Dictionary containing intent classification and parameters.

        Raises:
            ValueError: If the message is empty or invalid.
        """
        if not message.strip():
            raise ValueError("Message cannot be empty")

        logger.info(f"Processing message: {message}")

        intent = self._classify_intent(message)
        parameters = self._extract_parameters(message, intent)

        return {
            "intent": intent,
            "parameters": parameters,
            "confidence": self._calculate_confidence(message, intent)
        }
```

### Formatting Tools

We use the following tools for code formatting:

```bash
# Format code with Black
black src/ tests/

# Sort imports with isort
isort src/ tests/

# Type checking with mypy
mypy src/

# Linting with flake8
flake8 src/ tests/
```

### Pre-commit Hooks

Our pre-commit configuration automatically runs:

- Black (code formatting)
- isort (import sorting)
- flake8 (linting)
- mypy (type checking)
- pytest (basic tests)

## Testing Requirements

### Test Structure

```text
tests/
├── unit/                 # Unit tests for individual components
│   ├── test_intent_processor.py
│   ├── test_workflow_orchestrator.py
│   └── test_comfyui_client.py
├── integration/          # Integration tests
│   ├── test_comfyui_integration.py
│   └── test_chat_flow.py
├── fixtures/            # Test data and fixtures
│   ├── sample_workflows.json
│   └── test_images/
└── conftest.py          # Pytest configuration
```

### Writing Tests

#### Unit Tests

```python
import pytest
from unittest.mock import Mock, AsyncMock
from src.intent_processing import IntentProcessor

class TestIntentProcessor:
    @pytest.fixture
    def processor(self):
        return IntentProcessor()

    @pytest.mark.asyncio
    async def test_process_image_generation_intent(self, processor):
        """Test that image generation intents are correctly classified."""
        message = "Generate a red sports car"

        result = await processor.process(message)

        assert result["intent"] == "image_generation"
        assert "red sports car" in result["parameters"]["prompt"]
        assert result["confidence"] > 0.5

    def test_extract_style_from_message(self, processor):
        """Test style extraction from natural language."""
        message = "create an artistic painting of a landscape"

        style = processor._extract_style(message)

        assert style == "artistic"
```

#### Integration Tests

```python
import pytest
import asyncio
from src.main import ChatAIComfyUIApp

class TestComfyUIIntegration:
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_full_generation_workflow(self):
        """Test complete workflow from chat to image generation."""
        app = ChatAIComfyUIApp()
        await app.initialize()

        result = await app.chat_manager.process_message(
            user_id="test_user",
            message="Generate a simple landscape",
            platform="test"
        )

        assert result["success"] is True
        assert "prompt_id" in result["data"]
```

### Test Coverage

We aim for:

- **Unit tests**: 90%+ coverage
- **Integration tests**: Cover all major user flows
- **Performance tests**: For critical paths

Run coverage reports:

```bash
# Generate coverage report
pytest --cov=src tests/

# Generate HTML coverage report
pytest --cov=src --cov-report=html tests/
```

## Documentation

### Documentation Types

1. **Code Documentation**: Docstrings and inline comments
2. **API Documentation**: REST API and WebSocket API docs
3. **User Guides**: Setup, configuration, and usage guides
4. **Developer Guides**: Architecture and contribution docs

### Writing Documentation

#### Docstring Example

```python
def create_workflow_from_template(
    self,
    template_name: str,
    parameters: Dict[str, Any]
) -> Dict[str, Any]:
    """Create a ComfyUI workflow from a template.

    Takes a workflow template and fills in the parameters to create
    a complete workflow ready for execution.

    Args:
        template_name: Name of the workflow template to use.
        parameters: Dictionary of parameters to fill into the template.
            Expected keys:
            - prompt (str): The text prompt for generation
            - style (str, optional): Style modifier for the prompt
            - nsfw_filter (bool, optional): Whether to apply NSFW filtering

    Returns:
        Complete workflow dictionary ready for ComfyUI execution.

    Raises:
        KeyError: If the template_name is not found.
        ValueError: If required parameters are missing.

    Example:
        >>> orchestrator = WorkflowOrchestrator(client)
        >>> workflow = orchestrator.create_workflow_from_template(
        ...     "basic_generation",
        ...     {"prompt": "a red car", "style": "realistic"}
        ... )
        >>> print(workflow["2"]["inputs"]["text"])
        "a red car"
    """
```

#### Markdown Documentation

- Use clear headings and structure
- Include code examples for all features
- Add screenshots for UI components
- Keep examples up-to-date with the current API

## Pull Request Process

### Before Submitting

1. **Ensure tests pass**: All tests must pass locally
2. **Update documentation**: Include relevant documentation updates
3. **Add changelog entry**: Update CHANGELOG.md if applicable
4. **Rebase on main**: Ensure your branch is up-to-date

### PR Template

When creating a pull request, use this template:

```markdown
## Description
Brief description of the changes and their purpose.

## Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed
- [ ] Performance impact assessed

## Checklist
- [ ] Code follows the project's style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added for new functionality
- [ ] All tests pass locally
- [ ] No new linting errors introduced

## Screenshots (if applicable)
Add screenshots to help explain your changes.

## Additional Notes
Any additional information or context about the changes.
```

### Review Process

1. **Automated checks**: CI/CD pipeline runs tests and checks
2. **Code review**: At least one maintainer reviews the code
3. **Testing**: Changes are tested in a staging environment
4. **Approval**: PR is approved and merged

### Merge Requirements

- All CI checks must pass
- At least one approving review from a maintainer
- No merge conflicts with the main branch
- Documentation is up-to-date

## Issue Reporting

### Bug Reports

When reporting bugs, include:

1. **Environment details**: OS, Python version, ComfyUI version
2. **Steps to reproduce**: Clear, numbered steps
3. **Expected behavior**: What should happen
4. **Actual behavior**: What actually happens
5. **Error messages**: Full error messages and stack traces
6. **Screenshots**: If applicable

### Feature Requests

For feature requests, include:

1. **Problem description**: What problem does this solve?
2. **Proposed solution**: How should it work?
3. **Alternatives considered**: Other approaches you've thought about
4. **Use cases**: Specific scenarios where this would be useful

### Issue Templates

We provide templates for:

- Bug reports
- Feature requests
- Documentation improvements
- Performance issues

## Community

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and community discussion
- **Discord**: Real-time chat and support (if available)

### Getting Help

If you need help:

1. Check the [documentation](docs/)
2. Search existing [GitHub issues](https://github.com/tqer39/my-chat-ai-comfyui/issues)
3. Ask in [GitHub Discussions](https://github.com/tqer39/my-chat-ai-comfyui/discussions)
4. Join our community chat (if available)

### Recognition

Contributors are recognized in:

- CONTRIBUTORS.md file
- Release notes for significant contributions
- GitHub contributor graphs

## Development Workflow

### Typical Development Cycle

1. **Pick an issue** or create one for your idea
2. **Discuss the approach** in the issue comments
3. **Create a branch** from the latest main
4. **Implement the changes** following our guidelines
5. **Write tests** for your changes
6. **Update documentation** as needed
7. **Submit a pull request** with a clear description
8. **Address review feedback** promptly
9. **Celebrate** when your PR is merged! 🎉

### Release Process

We follow semantic versioning (SemVer):

- **Major** (X.0.0): Breaking changes
- **Minor** (0.X.0): New features, backwards compatible
- **Patch** (0.0.X): Bug fixes, backwards compatible

### Maintenance

The project is actively maintained by:

- Core maintainers who review PRs and manage releases
- Community contributors who help with features and bug fixes
- Documentation maintainers who keep docs up-to-date

Thank you for contributing to my-chat-ai-comfyui! Your contributions help make AI image generation more accessible to everyone.
