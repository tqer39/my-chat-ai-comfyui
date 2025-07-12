# API Documentation

This document provides comprehensive API documentation for the my-chat-ai-comfyui integration system.

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [REST API Endpoints](#rest-api-endpoints)
4. [WebSocket API](#websocket-api)
5. [ComfyUI Integration](#comfyui-integration)
6. [Error Handling](#error-handling)
7. [Rate Limiting](#rate-limiting)
8. [Examples](#examples)

## Overview

The my-chat-ai-comfyui system provides both REST and WebSocket APIs for integrating chat AI capabilities with ComfyUI workflows. The API allows you to:

- Process natural language commands
- Generate images through ComfyUI workflows
- Apply NSFW filtering and content safety measures
- Monitor generation progress in real-time
- Manage user sessions and conversation history

### Base URL

```
http://localhost:8080/api/v1
```

### Content Type

All API requests should use `application/json` content type unless otherwise specified.

## Authentication

### API Key Authentication

Include your API key in the request headers:

```http
Authorization: Bearer YOUR_API_KEY
```

### Session-based Authentication

For web interface integration, session-based authentication is also supported.

## REST API Endpoints

### Chat Processing

#### POST /chat/process

Process a natural language message and execute corresponding ComfyUI operations.

**Request Body:**
```json
{
  "message": "Generate a red sports car with dramatic lighting",
  "user_id": "user123",
  "platform": "web",
  "options": {
    "nsfw_filter": true,
    "style": "realistic",
    "quality": "high"
  }
}
```

**Response:**
```json
{
  "success": true,
  "response": "Image generated successfully!",
  "data": {
    "prompt_id": "abc123",
    "intent": "image_generation",
    "parameters": {
      "prompt": "red sports car with dramatic lighting",
      "style": "realistic",
      "nsfw_filter": true
    },
    "estimated_time": 30
  }
}
```

### Generation Management

#### GET /generation/status/{prompt_id}

Get the status of a specific generation request.

**Response:**
```json
{
  "prompt_id": "abc123",
  "status": "completed",
  "progress": 100,
  "outputs": {
    "images": [
      {
        "filename": "chat_ai_generated_00001_.png",
        "url": "/outputs/chat_ai_generated_00001_.png"
      }
    ]
  }
}
```

#### GET /generation/queue

Get the current generation queue status.

**Response:**
```json
{
  "queue_running": [
    {
      "prompt_id": "def456",
      "position": 1,
      "estimated_time": 45
    }
  ],
  "queue_pending": [
    {
      "prompt_id": "ghi789",
      "position": 2,
      "estimated_time": 90
    }
  ]
}
```

### Model Management

#### GET /models/list

List available ComfyUI models.

**Response:**
```json
{
  "checkpoints": [
    "sd3.5_medium.safetensors",
    "sd_xl_base_1.0.safetensors"
  ],
  "loras": [
    "style_lora_v1.safetensors"
  ],
  "controlnets": [
    "control_v11p_sd15_canny.pth"
  ]
}
```

### NSFW Filtering

#### POST /nsfw/analyze

Analyze an image for NSFW content.

**Request Body:**
```json
{
  "image_url": "/outputs/image.png",
  "confidence_threshold": 0.7
}
```

**Response:**
```json
{
  "is_nsfw": false,
  "confidence": 0.3,
  "detected_labels": [],
  "safe_for_work": true
}
```

#### POST /nsfw/filter

Apply NSFW filtering to an image.

**Request Body:**
```json
{
  "image_url": "/outputs/image.png",
  "method": "blur",
  "intensity": 0.8
}
```

**Response:**
```json
{
  "filtered_image_url": "/outputs/filtered_image.png",
  "method_applied": "blur",
  "areas_filtered": 2
}
```

## WebSocket API

### Connection

Connect to the WebSocket endpoint for real-time updates:

```
ws://localhost:8080/ws
```

### Message Format

All WebSocket messages use JSON format:

```json
{
  "type": "message_type",
  "data": { ... }
}
```

### Message Types

#### Client to Server

**chat_message:**
```json
{
  "type": "chat_message",
  "data": {
    "message": "Generate a landscape image",
    "user_id": "user123"
  }
}
```

**subscribe_generation:**
```json
{
  "type": "subscribe_generation",
  "data": {
    "prompt_id": "abc123"
  }
}
```

#### Server to Client

**generation_progress:**
```json
{
  "type": "generation_progress",
  "data": {
    "prompt_id": "abc123",
    "progress": 45,
    "current_step": "sampling",
    "estimated_remaining": 25
  }
}
```

**generation_complete:**
```json
{
  "type": "generation_complete",
  "data": {
    "prompt_id": "abc123",
    "outputs": {
      "images": ["/outputs/image.png"]
    }
  }
}
```

**chat_response:**
```json
{
  "type": "chat_response",
  "data": {
    "response": "I've started generating your landscape image!",
    "prompt_id": "abc123"
  }
}
```

## ComfyUI Integration

### Workflow Templates

The system uses predefined workflow templates that can be customized:

#### Basic Generation Template

```json
{
  "1": {
    "class_type": "CheckpointLoaderSimple",
    "inputs": {
      "ckpt_name": "{model}"
    }
  },
  "2": {
    "class_type": "CLIPTextEncode",
    "inputs": {
      "text": "{prompt}",
      "clip": ["1", 1]
    }
  }
}
```

#### NSFW Filtered Template

Includes additional nodes for content filtering:

```json
{
  "7": {
    "class_type": "NudenetModelLoader",
    "inputs": {}
  },
  "8": {
    "class_type": "ApplyNudenet",
    "inputs": {
      "image": ["6", 0],
      "model": ["7", 0],
      "confidence": 0.7,
      "censoring_method": "blur"
    }
  }
}
```

### Custom Workflows

#### POST /workflows/create

Create a custom workflow template.

**Request Body:**
```json
{
  "name": "custom_portrait",
  "description": "Custom portrait generation workflow",
  "workflow": { ... },
  "parameters": [
    {
      "name": "style",
      "type": "string",
      "default": "realistic"
    }
  ]
}
```

#### GET /workflows/list

List available workflow templates.

## Error Handling

### Error Response Format

```json
{
  "success": false,
  "error": {
    "code": "INVALID_PROMPT",
    "message": "The provided prompt contains invalid characters",
    "details": {
      "invalid_chars": ["<", ">"]
    }
  }
}
```

### Common Error Codes

- `INVALID_PROMPT`: Prompt validation failed
- `MODEL_NOT_FOUND`: Requested model is not available
- `GENERATION_FAILED`: ComfyUI generation failed
- `NSFW_DETECTED`: Content blocked by NSFW filter
- `QUEUE_FULL`: Generation queue is at capacity
- `RATE_LIMITED`: Request rate limit exceeded
- `UNAUTHORIZED`: Invalid or missing API key

## Rate Limiting

### Limits

- **Chat messages**: 60 requests per minute per user
- **Generation requests**: 10 requests per minute per user
- **Status checks**: 120 requests per minute per user

### Headers

Rate limit information is included in response headers:

```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1640995200
```

## Examples

### Python Client Example

```python
import requests
import json

class ChatAIComfyUIClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def generate_image(self, prompt, user_id="default"):
        data = {
            "message": prompt,
            "user_id": user_id,
            "platform": "api",
            "options": {
                "nsfw_filter": True,
                "quality": "high"
            }
        }

        response = requests.post(
            f"{self.base_url}/chat/process",
            headers=self.headers,
            json=data
        )

        return response.json()

    def check_status(self, prompt_id):
        response = requests.get(
            f"{self.base_url}/generation/status/{prompt_id}",
            headers=self.headers
        )

        return response.json()

client = ChatAIComfyUIClient("http://localhost:8080/api/v1", "your_api_key")
result = client.generate_image("A beautiful sunset over mountains")
print(result)
```

### JavaScript Client Example

```javascript
class ChatAIComfyUIClient {
    constructor(baseUrl, apiKey) {
        this.baseUrl = baseUrl;
        this.apiKey = apiKey;
    }

    async generateImage(prompt, userId = 'default') {
        const response = await fetch(`${this.baseUrl}/chat/process`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${this.apiKey}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: prompt,
                user_id: userId,
                platform: 'web',
                options: {
                    nsfw_filter: true,
                    quality: 'high'
                }
            })
        });

        return await response.json();
    }

    async checkStatus(promptId) {
        const response = await fetch(`${this.baseUrl}/generation/status/${promptId}`, {
            headers: {
                'Authorization': `Bearer ${this.apiKey}`
            }
        });

        return await response.json();
    }
}

const client = new ChatAIComfyUIClient('http://localhost:8080/api/v1', 'your_api_key');
client.generateImage('A serene lake at dawn').then(console.log);
```

### WebSocket Client Example

```javascript
const ws = new WebSocket('ws://localhost:8080/ws');

ws.onopen = function() {
    console.log('Connected to WebSocket');

    ws.send(JSON.stringify({
        type: 'chat_message',
        data: {
            message: 'Generate a fantasy castle',
            user_id: 'user123'
        }
    }));
};

ws.onmessage = function(event) {
    const message = JSON.parse(event.data);

    switch(message.type) {
        case 'chat_response':
            console.log('Chat response:', message.data.response);
            break;
        case 'generation_progress':
            console.log('Progress:', message.data.progress + '%');
            break;
        case 'generation_complete':
            console.log('Generation complete:', message.data.outputs);
            break;
    }
};
```

## SDK and Libraries

### Official Python SDK

```bash
pip install my-chat-ai-comfyui-sdk
```

### Community Libraries

- **Node.js**: `npm install comfyui-chat-client`
- **PHP**: `composer require comfyui/chat-client`
- **Go**: `go get github.com/comfyui/chat-client-go`

For more examples and detailed integration guides, see the [HOWTO documentation](HOWTO.md).
