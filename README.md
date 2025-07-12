# My Chat AI ComfyUI

A powerful integration system that bridges conversational AI interfaces with ComfyUI's visual programming environment for Stable Diffusion workflows. This project enables users to control complex image generation pipelines through natural language commands, democratizing access to advanced AI image generation capabilities.

## 🚀 Features

- **Natural Language Processing**: Convert chat commands into structured ComfyUI workflow operations
- **NSFW Content Management**: Integrated ComfyUI-Nudenet for intelligent content filtering and safety
- **Multi-Platform Chat Integration**: Support for Discord, Slack, web interfaces, and custom chatbots
- **Dynamic Workflow Creation**: Generate and modify ComfyUI workflows based on conversational input
- **Real-time Execution Monitoring**: Track workflow progress and provide user feedback
- **Intelligent Parameter Extraction**: Automatically parse and map parameters from natural language

## 🎯 Target Users

- **End Users**: Generate and manipulate images using natural language instead of complex visual programming
- **Developers**: Build chat-based applications with advanced image generation capabilities
- **AI Artists**: Use conversational interfaces for iterating on image generation workflows
- **Content Creators**: Safely generate content with built-in NSFW filtering and management

## 📋 Prerequisites

- Windows 11 (recommended) or Windows 10
- Python 3.8 or higher
- ComfyUI installation
- Git for version control
- PowerShell (for automated setup)

## 🛠️ Quick Start

### Automated Setup (Windows 11)

1. Clone the repository:
```bash
git clone https://github.com/tqer39/my-chat-ai-comfyui.git
cd my-chat-ai-comfyui
```

2. Run the automated setup script:
```powershell
.\setup.ps1
```

### Manual Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Configure ComfyUI integration:
```bash
python src/setup_comfyui.py
```

3. Set up environment variables:
```bash
cp config/example.env .env
# Edit .env with your configuration
```

## 📚 Documentation

- [**HOWTO Guide**](docs/HOWTO.md) - Comprehensive setup and usage instructions
- [**API Documentation**](docs/API.md) - Developer reference for integration
- [**Contributing Guide**](docs/CONTRIBUTING.md) - Guidelines for contributors
- [**Configuration Guide**](docs/CONFIGURATION.md) - Advanced configuration options

## 🔧 Core Components

### Chat Interface Layer
- Message reception and validation
- Multi-platform chat system integration
- Response formatting and delivery

### Intent Processing Engine
- Natural language understanding (NLU)
- Command classification and entity recognition
- Parameter extraction and validation

### ComfyUI Control Layer
- API client for ComfyUI operations
- Workflow management and execution
- Node manipulation and configuration

### NSFW Safety System
- ComfyUI-Nudenet integration
- Content filtering and censoring
- Customizable safety thresholds

## 🚦 Usage Examples

### Basic Image Generation
```
User: "Generate a red sports car with dramatic lighting"
System: Creates ComfyUI workflow → Executes → Returns generated image
```

### NSFW Content Filtering
```
User: "Create an artistic portrait"
System: Generates image → Applies NSFW filtering → Returns safe content
```

### Workflow Modification
```
User: "Make the previous image more vibrant and add a sunset background"
System: Modifies existing workflow → Re-executes → Returns updated image
```

## 🔒 Safety Features

- **Automatic NSFW Detection**: Uses ComfyUI-Nudenet for content analysis
- **Customizable Filtering**: Adjust sensitivity and filtering methods
- **Content Censoring**: Multiple censoring options (blur, pixelation, overlay)
- **Audit Logging**: Track all generated content for compliance

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/CONTRIBUTING.md) for details on:
- Code style and standards
- Development workflow
- Testing requirements
- Pull request process

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check our [HOWTO guide](docs/HOWTO.md) for common issues
- **Issues**: Report bugs and feature requests on [GitHub Issues](https://github.com/tqer39/my-chat-ai-comfyui/issues)
- **Discussions**: Join our community discussions for help and ideas

## 🔗 Related Projects

- [ComfyUI](https://github.com/comfyanonymous/ComfyUI) - The powerful visual AI engine
- [ComfyUI-Nudenet](https://github.com/phuvinh010701/ComfyUI-Nudenet) - NSFW content filtering extension
- [RunComfy](https://www.runcomfy.com/) - Online ComfyUI platform and resources

---

**Note**: This project is designed to work with ComfyUI's API and requires a properly configured ComfyUI installation. Please refer to the [HOWTO guide](docs/HOWTO.md) for detailed setup instructions.
