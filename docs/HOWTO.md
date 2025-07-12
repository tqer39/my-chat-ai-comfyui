# ComfyUI NSFW Setup Guide

This comprehensive guide will walk you through setting up ComfyUI with NSFW content filtering capabilities and integrating it with the my-chat-ai-comfyui system.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [ComfyUI Installation](#comfyui-installation)
3. [ComfyUI-Nudenet Setup](#comfyui-nudenet-setup)
4. [Model Configuration](#model-configuration)
5. [Chat AI Integration](#chat-ai-integration)
6. [Workflow Examples](#workflow-examples)
7. [Troubleshooting](#troubleshooting)
8. [Advanced Configuration](#advanced-configuration)

## Prerequisites

### System Requirements

- **Operating System**: Windows 11 (recommended), Windows 10, or Linux
- **Python**: Version 3.8 or higher
- **GPU**: NVIDIA GPU with at least 6GB VRAM (recommended)
- **RAM**: Minimum 16GB system RAM
- **Storage**: At least 50GB free space for models and outputs

### Required Software

- Git for version control
- Python with pip package manager
- PowerShell (Windows) or Bash (Linux)
- Text editor or IDE

## ComfyUI Installation

### Method 1: Automated Installation (Windows 11)

1. **Download ComfyUI Portable**:
   ```powershell
   # Download the latest ComfyUI portable version
   Invoke-WebRequest -Uri "https://github.com/comfyanonymous/ComfyUI/releases/latest/download/ComfyUI_windows_portable_nvidia_cu121_or_cpu.7z" -OutFile "ComfyUI_portable.7z"
   ```

2. **Extract and Setup**:
   ```powershell
   # Extract to your preferred directory
   7z x ComfyUI_portable.7z -o"C:\ComfyUI"
   cd C:\ComfyUI
   ```

3. **Run ComfyUI**:
   ```powershell
   .\run_nvidia_gpu.bat
   ```

### Method 2: Manual Installation

1. **Clone ComfyUI Repository**:
   ```bash
   git clone https://github.com/comfyanonymous/ComfyUI.git
   cd ComfyUI
   ```

2. **Install Dependencies**:
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
   pip install -r requirements.txt
   ```

3. **Launch ComfyUI**:
   ```bash
   python main.py
   ```

## ComfyUI-Nudenet Setup

### Installation via ComfyUI Manager

1. **Access ComfyUI Manager**:
   - Open ComfyUI in your browser (usually http://localhost:8188)
   - Click the "Manager" button in the main menu

2. **Install ComfyUI-Nudenet**:
   - Select "Custom Nodes Manager" button
   - Search for "ComfyUI-Nudenet" in the search bar
   - Click "Install" next to the ComfyUI-Nudenet extension
   - Click "Restart" to restart ComfyUI

3. **Verify Installation**:
   - Refresh your browser to clear cache
   - Check that Nudenet nodes appear in the node list

### Manual Installation

1. **Clone the Extension**:
   ```bash
   cd ComfyUI/custom_nodes
   git clone https://github.com/phuvinh010701/ComfyUI-Nudenet.git
   ```

2. **Install Dependencies**:
   ```bash
   cd ComfyUI-Nudenet
   pip install -r requirements.txt
   ```

3. **Restart ComfyUI**:
   ```bash
   # Stop ComfyUI and restart
   python main.py
   ```

## Model Configuration

### Download Required Models

1. **Base Stable Diffusion Models**:
   ```bash
   # Download to ComfyUI/models/checkpoints/
   # Example: Stable Diffusion 3.5 Medium (requires license acceptance)
   # Visit https://huggingface.co/stabilityai/stable-diffusion-3.5-medium
   ```

2. **NSFW Detection Model**:
   ```bash
   # The Nudenet model will be automatically downloaded on first use
   # It will be placed in ComfyUI/models/Nudenet/
   ```

### Model Directory Structure

```
ComfyUI/
├── models/
│   ├── checkpoints/          # Stable Diffusion models
│   ├── vae/                  # VAE models
│   ├── loras/                # LoRA models
│   ├── controlnet/           # ControlNet models
│   └── Nudenet/              # NSFW detection models
├── custom_nodes/
│   └── ComfyUI-Nudenet/      # NSFW filtering extension
└── output/                   # Generated images
```

## Chat AI Integration

### Environment Setup

1. **Create Configuration File**:
   ```bash
   cp config/example.env .env
   ```

2. **Configure Environment Variables**:
   ```env
   # ComfyUI Configuration
   COMFYUI_HOST=localhost
   COMFYUI_PORT=8188
   COMFYUI_API_ENDPOINT=http://localhost:8188

   # Chat AI Configuration
   OPENAI_API_KEY=your_openai_api_key_here
   DISCORD_BOT_TOKEN=your_discord_token_here
   SLACK_BOT_TOKEN=your_slack_token_here

   # NSFW Filtering Configuration
   NSFW_DETECTION_ENABLED=true
   NSFW_CONFIDENCE_THRESHOLD=0.7
   NSFW_CENSORING_METHOD=blur
   ```

### API Integration

1. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Test ComfyUI API Connection**:
   ```python
   python src/test_comfyui_connection.py
   ```

3. **Start Chat AI Service**:
   ```bash
   python src/main.py
   ```

## Workflow Examples

### Basic NSFW-Filtered Image Generation

1. **Create Workflow**:
   - Load your preferred Stable Diffusion model
   - Add text prompt input
   - Connect to image generation nodes
   - Add Nudenet Model Loader
   - Connect Apply Nudenet node
   - Configure filtering parameters

2. **Example Workflow JSON**:
   ```json
   {
     "1": {
       "class_type": "CheckpointLoaderSimple",
       "inputs": {
         "ckpt_name": "sd3.5_medium.safetensors"
       }
     },
     "2": {
       "class_type": "CLIPTextEncode",
       "inputs": {
         "text": "beautiful landscape, high quality",
         "clip": ["1", 1]
       }
     },
     "3": {
       "class_type": "NudenetModelLoader",
       "inputs": {}
     },
     "4": {
       "class_type": "ApplyNudenet",
       "inputs": {
         "image": ["generated_image", 0],
         "model": ["3", 0],
         "confidence": 0.7,
         "censoring_method": "blur"
       }
     }
   }
   ```

### Chat Command Processing

1. **Natural Language Input**:
   ```
   User: "Generate a portrait of a person in artistic style, make sure it's safe for work"
   ```

2. **System Processing**:
   - Parse intent: image generation
   - Extract parameters: portrait, person, artistic style
   - Apply safety filter: NSFW detection enabled
   - Generate ComfyUI workflow
   - Execute and return filtered result

## Troubleshooting

### Common Issues

#### ComfyUI Won't Start

**Problem**: ComfyUI fails to launch or crashes on startup.

**Solutions**:
1. Check Python version compatibility:
   ```bash
   python --version  # Should be 3.8+
   ```

2. Verify GPU drivers:
   ```bash
   nvidia-smi  # Check NVIDIA GPU status
   ```

3. Install missing dependencies:
   ```bash
   pip install --upgrade torch torchvision torchaudio
   ```

#### Nudenet Extension Not Working

**Problem**: NSFW filtering nodes don't appear or don't work.

**Solutions**:
1. Verify installation:
   ```bash
   ls ComfyUI/custom_nodes/ComfyUI-Nudenet/
   ```

2. Check dependencies:
   ```bash
   pip install onnxruntime opencv-python pillow
   ```

3. Restart ComfyUI completely:
   ```bash
   # Kill all ComfyUI processes and restart
   ```

#### Model Loading Errors

**Problem**: Models fail to load or cause out-of-memory errors.

**Solutions**:
1. Check available VRAM:
   ```bash
   nvidia-smi
   ```

2. Use smaller models or enable CPU offloading:
   ```bash
   python main.py --cpu
   ```

3. Verify model file integrity:
   ```bash
   # Re-download corrupted models
   ```

### Performance Optimization

#### GPU Memory Management

1. **Enable Model Offloading**:
   ```bash
   python main.py --normalvram
   ```

2. **Use Attention Optimization**:
   ```bash
   python main.py --use-split-cross-attention
   ```

#### NSFW Detection Optimization

1. **Adjust Confidence Threshold**:
   - Lower values: More sensitive detection
   - Higher values: Less false positives

2. **Optimize Censoring Methods**:
   - Blur: Fast, good for most content
   - Pixelation: More obvious censoring
   - Overlay: Custom image overlay

## Advanced Configuration

### Custom NSFW Labels

Configure which content types to filter:

```python
# In your configuration
NSFW_LABELS = [
    "EXPOSED_ANUS",
    "EXPOSED_ARMPITS", 
    "EXPOSED_BELLY",
    "EXPOSED_BUTTOCKS",
    "EXPOSED_BREAST_F",
    "EXPOSED_GENITALIA_F",
    "EXPOSED_GENITALIA_M"
]
```

### Workflow Templates

Create reusable workflow templates for common use cases:

1. **Safe Portrait Generation**
2. **Landscape with NSFW Check**
3. **Artistic Style Transfer with Filtering**
4. **Batch Processing with Safety**

### API Endpoints

The system provides REST API endpoints for integration:

```
POST /api/generate
POST /api/filter
GET /api/status
GET /api/models
```

### Monitoring and Logging

Enable comprehensive logging for debugging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Security Considerations

1. **API Security**: Use authentication tokens for API access
2. **Content Logging**: Log filtered content for audit purposes
3. **User Permissions**: Implement role-based access control
4. **Data Privacy**: Ensure generated content is handled securely

## Next Steps

After completing this setup:

1. Test the complete pipeline with sample prompts
2. Configure your preferred chat platforms
3. Customize NSFW filtering parameters
4. Set up monitoring and logging
5. Deploy to your production environment

For additional help, refer to the [API Documentation](API.md) or [Contributing Guide](CONTRIBUTING.md).
