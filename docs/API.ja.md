# My Chat AI ComfyUI API ドキュメント

このドキュメントでは、my-chat-ai-comfyui統合システムで利用可能なREST APIとWebSocket APIについて詳しく説明します。

## 目次

1. [概要](#概要)
2. [認証](#認証)
3. [REST API](#rest-api)
4. [WebSocket API](#websocket-api)
5. [エラーハンドリング](#エラーハンドリング)
6. [レート制限](#レート制限)
7. [使用例](#使用例)
8. [SDK とライブラリ](#sdk-とライブラリ)

## 概要

My Chat AI ComfyUI APIは、会話型AIインターフェースとComfyUIの視覚的プログラミング環境を統合するための包括的なAPIセットを提供します。

### ベースURL

```text
https://api.my-chat-ai-comfyui.com/v1
```

### サポートされる形式

- **リクエスト**: JSON
- **レスポンス**: JSON
- **WebSocket**: JSON メッセージ

## 認証

### APIキー認証

すべてのAPIリクエストには有効なAPIキーが必要です。

```http
Authorization: Bearer YOUR_API_KEY
```

### APIキーの取得

1. アカウントダッシュボードにログイン
2. 「API Keys」セクションに移動
3. 新しいAPIキーを生成
4. キーを安全に保存

## REST API

### チャット処理

#### POST /api/chat/process

自然言語メッセージを処理し、ComfyUIワークフローを生成・実行します。

**リクエスト**:

```json
{
  "message": "美しい風景画像を生成してください",
  "user_id": "user123",
  "session_id": "session456",
  "options": {
    "nsfw_filter": true,
    "style": "realistic",
    "quality": "high"
  }
}
```

**レスポンス**:

```json
{
  "success": true,
  "request_id": "req_789",
  "prompt_id": "prompt_abc",
  "estimated_time": 30,
  "status": "queued",
  "message": "画像生成を開始しました"
}
```

#### GET /api/chat/history

チャット履歴を取得します。

**パラメータ**:

- `user_id` (必須): ユーザーID
- `session_id` (オプション): セッションID
- `limit` (オプション): 取得する履歴の数（デフォルト: 50）
- `offset` (オプション): オフセット（デフォルト: 0）

**レスポンス**:

```json
{
  "success": true,
  "history": [
    {
      "id": "msg_001",
      "timestamp": "2025-01-12T10:30:00Z",
      "message": "美しい風景画像を生成してください",
      "response": "画像を生成しました",
      "images": ["https://example.com/image1.jpg"]
    }
  ],
  "total": 25,
  "has_more": false
}
```

### 生成管理

#### GET /api/generation/status/{prompt_id}

生成ステータスを確認します。

**レスポンス**:

```json
{
  "success": true,
  "prompt_id": "prompt_abc",
  "status": "completed",
  "progress": 100,
  "estimated_remaining": 0,
  "results": [
    {
      "type": "image",
      "url": "https://example.com/generated_image.jpg",
      "metadata": {
        "width": 1024,
        "height": 1024,
        "seed": 12345
      }
    }
  ]
}
```

#### POST /api/generation/cancel/{prompt_id}

生成をキャンセルします。

**レスポンス**:

```json
{
  "success": true,
  "message": "生成がキャンセルされました",
  "prompt_id": "prompt_abc"
}
```

#### GET /api/generation/queue

現在のキューの状態を取得します。

**レスポンス**:

```json
{
  "success": true,
  "queue": {
    "pending": 3,
    "running": 1,
    "completed_today": 127
  },
  "estimated_wait_time": 45
}
```

### モデル管理

#### GET /api/models/list

利用可能なモデルのリストを取得します。

**パラメータ**:

- `type` (オプション): モデルタイプ（checkpoint, lora, vae, etc.）
- `category` (オプション): カテゴリ（realistic, anime, artistic, etc.）

**レスポンス**:

```json
{
  "success": true,
  "models": [
    {
      "id": "sd35_medium",
      "name": "Stable Diffusion 3.5 Medium",
      "type": "checkpoint",
      "category": "realistic",
      "description": "高品質な写実的画像生成モデル",
      "file_size": "5.2GB",
      "supported_resolutions": ["1024x1024", "1152x896", "896x1152"]
    }
  ]
}
```

#### GET /api/models/info/{model_id}

特定のモデルの詳細情報を取得します。

**レスポンス**:

```json
{
  "success": true,
  "model": {
    "id": "sd35_medium",
    "name": "Stable Diffusion 3.5 Medium",
    "version": "1.0",
    "type": "checkpoint",
    "category": "realistic",
    "description": "高品質な写実的画像生成モデル",
    "parameters": {
      "base_resolution": "1024x1024",
      "max_resolution": "2048x2048",
      "recommended_steps": 28,
      "recommended_cfg": 7.0
    },
    "license": "CreativeML Open RAIL-M",
    "created_at": "2024-10-15T00:00:00Z"
  }
}
```

### NSFWフィルタリング

#### POST /api/nsfw/analyze

画像のNSFWコンテンツを分析します。

**リクエスト**:

```json
{
  "image_url": "https://example.com/image.jpg",
  "confidence_threshold": 0.7
}
```

**レスポンス**:

```json
{
  "success": true,
  "analysis": {
    "is_nsfw": false,
    "confidence": 0.95,
    "labels": [
      {
        "label": "SAFE",
        "confidence": 0.95
      }
    ],
    "filtered_image_url": null
  }
}
```

#### POST /api/nsfw/filter

画像にNSFWフィルターを適用します。

**リクエスト**:

```json
{
  "image_url": "https://example.com/image.jpg",
  "filter_method": "blur",
  "confidence_threshold": 0.7
}
```

**レスポンス**:

```json
{
  "success": true,
  "filtered_image_url": "https://example.com/filtered_image.jpg",
  "filter_applied": true,
  "filter_method": "blur"
}
```

### ワークフロー管理

#### GET /api/workflows/templates

利用可能なワークフローテンプレートを取得します。

**レスポンス**:

```json
{
  "success": true,
  "templates": [
    {
      "id": "basic_generation",
      "name": "基本画像生成",
      "description": "シンプルなテキストから画像への生成",
      "category": "basic",
      "parameters": [
        {
          "name": "prompt",
          "type": "string",
          "required": true,
          "description": "生成プロンプト"
        }
      ]
    }
  ]
}
```

#### POST /api/workflows/execute

カスタムワークフローを実行します。

**リクエスト**:

```json
{
  "workflow": {
    "1": {
      "class_type": "CheckpointLoaderSimple",
      "inputs": {
        "ckpt_name": "sd3.5_medium.safetensors"
      }
    }
  },
  "parameters": {
    "prompt": "美しい風景"
  }
}
```

## WebSocket API

### 接続

```javascript
const ws = new WebSocket('wss://api.my-chat-ai-comfyui.com/v1/ws');
```

### WebSocket認証

接続後、最初にAPIキーで認証を行います：

```json
{
  "type": "auth",
  "api_key": "YOUR_API_KEY"
}
```

### メッセージタイプ

#### 生成進捗の購読

```json
{
  "type": "subscribe",
  "channel": "generation_progress",
  "prompt_id": "prompt_abc"
}
```

#### 進捗更新の受信

```json
{
  "type": "progress_update",
  "prompt_id": "prompt_abc",
  "progress": 45,
  "stage": "sampling",
  "estimated_remaining": 15
}
```

#### 完了通知の受信

```json
{
  "type": "generation_complete",
  "prompt_id": "prompt_abc",
  "results": [
    {
      "type": "image",
      "url": "https://example.com/result.jpg"
    }
  ]
}
```

## エラーハンドリング

### エラーレスポンス形式

```json
{
  "success": false,
  "error": {
    "code": "INVALID_PROMPT",
    "message": "プロンプトが無効です",
    "details": "プロンプトは1文字以上1000文字以下である必要があります"
  },
  "request_id": "req_789"
}
```

### 一般的なエラーコード

| コード | 説明 |
|--------|------|
| `INVALID_API_KEY` | APIキーが無効または期限切れ |
| `RATE_LIMIT_EXCEEDED` | レート制限を超過 |
| `INVALID_PROMPT` | プロンプトが無効 |
| `MODEL_NOT_FOUND` | 指定されたモデルが見つからない |
| `GENERATION_FAILED` | 画像生成に失敗 |
| `NSFW_CONTENT_DETECTED` | NSFWコンテンツが検出された |
| `INSUFFICIENT_CREDITS` | クレジットが不足 |

## レート制限

### 制限

- **無料プラン**: 100リクエスト/時間
- **プロプラン**: 1,000リクエスト/時間
- **エンタープライズプラン**: カスタム制限

### レート制限ヘッダー

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1641024000
```

## 使用例

### Python

```python
import requests
import json

# APIクライアントの設定
API_BASE = "https://api.my-chat-ai-comfyui.com/v1"
API_KEY = "your_api_key_here"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 画像生成リクエスト
def generate_image(prompt):
    data = {
        "message": prompt,
        "user_id": "user123",
        "options": {
            "nsfw_filter": True,
            "style": "realistic"
        }
    }

    response = requests.post(
        f"{API_BASE}/api/chat/process",
        headers=headers,
        json=data
    )

    return response.json()

# 使用例
result = generate_image("美しい山の風景")
print(json.dumps(result, indent=2, ensure_ascii=False))
```

### JavaScript

```javascript
class ChatAIComfyUIClient {
    constructor(apiKey) {
        this.apiKey = apiKey;
        this.baseURL = 'https://api.my-chat-ai-comfyui.com/v1';
    }

    async generateImage(prompt, options = {}) {
        const response = await fetch(`${this.baseURL}/api/chat/process`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${this.apiKey}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: prompt,
                user_id: 'user123',
                options: {
                    nsfw_filter: true,
                    ...options
                }
            })
        });

        return await response.json();
    }

    async getGenerationStatus(promptId) {
        const response = await fetch(
            `${this.baseURL}/api/generation/status/${promptId}`,
            {
                headers: {
                    'Authorization': `Bearer ${this.apiKey}`
                }
            }
        );

        return await response.json();
    }
}

// 使用例
const client = new ChatAIComfyUIClient('your_api_key_here');

client.generateImage('美しい海の風景')
    .then(result => console.log(result))
    .catch(error => console.error(error));
```

### WebSocket クライアント

```javascript
class ChatAIWebSocketClient {
    constructor(apiKey) {
        this.apiKey = apiKey;
        this.ws = null;
    }

    connect() {
        this.ws = new WebSocket('wss://api.my-chat-ai-comfyui.com/v1/ws');

        this.ws.onopen = () => {
            // 認証
            this.ws.send(JSON.stringify({
                type: 'auth',
                api_key: this.apiKey
            }));
        };

        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleMessage(data);
        };
    }

    subscribeToProgress(promptId) {
        this.ws.send(JSON.stringify({
            type: 'subscribe',
            channel: 'generation_progress',
            prompt_id: promptId
        }));
    }

    handleMessage(data) {
        switch(data.type) {
            case 'progress_update':
                console.log(`進捗: ${data.progress}%`);
                break;
            case 'generation_complete':
                console.log('生成完了:', data.results);
                break;
        }
    }
}
```

## SDK とライブラリ

### 公式SDK

- **Python**: `pip install my-chat-ai-comfyui`
- **JavaScript/Node.js**: `npm install my-chat-ai-comfyui`
- **Go**: `go get github.com/my-chat-ai-comfyui/go-sdk`

### コミュニティライブラリ

- **Ruby**: `gem install chat_ai_comfyui`
- **PHP**: `composer require my-chat-ai-comfyui/php-sdk`
- **C#**: `dotnet add package MyChatAIComfyUI`

### 使用例（Python SDK）

```python
from my_chat_ai_comfyui import ChatAIClient

client = ChatAIClient(api_key="your_api_key")

# 画像生成
result = client.generate_image(
    prompt="美しい風景",
    style="realistic",
    nsfw_filter=True
)

# 進捗監視
for update in client.watch_progress(result.prompt_id):
    print(f"進捗: {update.progress}%")
    if update.completed:
        print("完了:", update.results)
        break
```

## サポートとフィードバック

- **ドキュメント**: [https://docs.my-chat-ai-comfyui.com](https://docs.my-chat-ai-comfyui.com)
- **サポート**: [support@my-chat-ai-comfyui.com](mailto:support@my-chat-ai-comfyui.com)
- **GitHub**: [https://github.com/tqer39/my-chat-ai-comfyui](https://github.com/tqer39/my-chat-ai-comfyui)
- **Discord**: [コミュニティサーバーに参加](https://discord.gg/my-chat-ai-comfyui)

APIの改善提案やバグレポートは、GitHubのIssuesまたはサポートメールまでお送りください。
