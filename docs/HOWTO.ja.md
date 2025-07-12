# ComfyUI NSFW セットアップガイド

この包括的なガイドでは、NSFWコンテンツフィルタリング機能を備えたComfyUIのセットアップと、my-chat-ai-comfyuiシステムとの統合について説明します。

## 目次

1. [前提条件](#前提条件)
2. [ComfyUIインストール](#comfyuiインストール)
3. [ComfyUI-Nudenetセットアップ](#comfyui-nudenetセットアップ)
4. [モデル設定](#モデル設定)
5. [チャットAI統合](#チャットai統合)
6. [ワークフロー例](#ワークフロー例)
7. [トラブルシューティング](#トラブルシューティング)
8. [高度な設定](#高度な設定)

## 前提条件

### システム要件

- **オペレーティングシステム**: Windows 11（推奨）、Windows 10、またはLinux
- **Python**: バージョン3.8以上
- **GPU**: 最低6GB VRAMのNVIDIA GPU（推奨）
- **RAM**: 最低16GBのシステムRAM
- **ストレージ**: モデルと出力用に最低50GBの空き容量

### 必要なソフトウェア

- バージョン管理用のGit
- pipパッケージマネージャー付きのPython
- PowerShell（Windows）またはBash（Linux）
- テキストエディターまたはIDE

## ComfyUIインストール

### 方法1: 自動インストール（Windows 11）

1. **ComfyUI Portableをダウンロード**:
   ```powershell
   # 最新のComfyUI portableバージョンをダウンロード
   Invoke-WebRequest -Uri "https://github.com/comfyanonymous/ComfyUI/releases/latest/download/ComfyUI_windows_portable_nvidia_cu121_or_cpu.7z" -OutFile "ComfyUI_portable.7z"
   ```

2. **展開とセットアップ**:
   ```powershell
   # 希望するディレクトリに展開
   7z x ComfyUI_portable.7z -o"C:\ComfyUI"
   cd C:\ComfyUI
   ```

3. **ComfyUIを実行**:
   ```powershell
   .\run_nvidia_gpu.bat
   ```

### 方法2: 手動インストール

1. **ComfyUIリポジトリをクローン**:
   ```bash
   git clone https://github.com/comfyanonymous/ComfyUI.git
   cd ComfyUI
   ```

2. **依存関係をインストール**:
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
   pip install -r requirements.txt
   ```

3. **ComfyUIを起動**:
   ```bash
   python main.py
   ```

## ComfyUI-Nudenetセットアップ

### ComfyUI Manager経由でのインストール

1. **ComfyUI Managerにアクセス**:
   - ブラウザでComfyUIを開く（通常はhttp://localhost:8188）
   - メインメニューの「Manager」ボタンをクリック

2. **ComfyUI-Nudenetをインストール**:
   - 「Custom Nodes Manager」ボタンを選択
   - 検索バーで「ComfyUI-Nudenet」を検索
   - ComfyUI-Nudenet拡張の横にある「Install」をクリック
   - 「Restart」をクリックしてComfyUIを再起動

3. **インストールを確認**:
   - ブラウザを更新してキャッシュをクリア
   - Nudenetノードがノードリストに表示されることを確認

### 手動インストール

1. **拡張をクローン**:
   ```bash
   cd ComfyUI/custom_nodes
   git clone https://github.com/phuvinh010701/ComfyUI-Nudenet.git
   ```

2. **依存関係をインストール**:
   ```bash
   cd ComfyUI-Nudenet
   pip install -r requirements.txt
   ```

3. **ComfyUIを再起動**:
   ```bash
   # ComfyUIを停止して再起動
   python main.py
   ```

## モデル設定

### 必要なモデルをダウンロード

1. **ベースStable Diffusionモデル**:
   ```bash
   # ComfyUI/models/checkpoints/にダウンロード
   # 例: Stable Diffusion 3.5 Medium（ライセンス承認が必要）
   # https://huggingface.co/stabilityai/stable-diffusion-3.5-mediumを訪問
   ```

2. **NSFW検出モデル**:
   ```bash
   # Nudenetモデルは初回使用時に自動的にダウンロードされます
   # ComfyUI/models/Nudenet/に配置されます
   ```

### モデルディレクトリ構造

```
ComfyUI/
├── models/
│   ├── checkpoints/          # Stable Diffusionモデル
│   ├── vae/                  # VAEモデル
│   ├── loras/                # LoRAモデル
│   ├── controlnet/           # ControlNetモデル
│   └── Nudenet/              # NSFW検出モデル
├── custom_nodes/
│   └── ComfyUI-Nudenet/      # NSFWフィルタリング拡張
└── output/                   # 生成された画像
```

## チャットAI統合

### 環境セットアップ

1. **設定ファイルを作成**:
   ```bash
   cp config/example.env .env
   ```

2. **環境変数を設定**:
   ```env
   # ComfyUI設定
   COMFYUI_HOST=localhost
   COMFYUI_PORT=8188
   COMFYUI_API_ENDPOINT=http://localhost:8188

   # チャットAI設定
   OPENAI_API_KEY=your_openai_api_key_here
   DISCORD_BOT_TOKEN=your_discord_token_here
   SLACK_BOT_TOKEN=your_slack_token_here

   # NSFWフィルタリング設定
   NSFW_DETECTION_ENABLED=true
   NSFW_CONFIDENCE_THRESHOLD=0.7
   NSFW_CENSORING_METHOD=blur
   ```

### API統合

1. **Python依存関係をインストール**:
   ```bash
   pip install -r requirements.txt
   ```

2. **ComfyUI API接続をテスト**:
   ```python
   python src/test_comfyui_connection.py
   ```

3. **チャットAIサービスを開始**:
   ```bash
   python src/main.py
   ```

## ワークフロー例

### 基本的なNSFWフィルタリング画像生成

1. **ワークフローを作成**:
   - 希望するStable Diffusionモデルを読み込み
   - テキストプロンプト入力を追加
   - 画像生成ノードに接続
   - Nudenet Model Loaderを追加
   - Apply Nudenetノードを接続
   - フィルタリングパラメータを設定

2. **ワークフローJSONの例**:
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
         "text": "美しい風景、高品質",
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

### チャットコマンド処理

1. **自然言語入力**:
   ```
   ユーザー: "芸術的なスタイルで人物のポートレートを生成して、職場で安全なものにしてください"
   ```

2. **システム処理**:
   - 意図を解析: 画像生成
   - パラメータを抽出: ポートレート、人物、芸術的スタイル
   - 安全フィルターを適用: NSFW検出を有効化
   - ComfyUIワークフローを生成
   - 実行してフィルタリングされた結果を返す

## トラブルシューティング

### よくある問題

#### ComfyUIが起動しない

**問題**: ComfyUIの起動に失敗するか、起動時にクラッシュする。

**解決策**:
1. Pythonバージョンの互換性を確認:
   ```bash
   python --version  # 3.8以上である必要があります
   ```

2. GPUドライバーを確認:
   ```bash
   nvidia-smi  # NVIDIA GPUの状態を確認
   ```

3. 不足している依存関係をインストール:
   ```bash
   pip install --upgrade torch torchvision torchaudio
   ```

#### Nudenet拡張が動作しない

**問題**: NSFWフィルタリングノードが表示されないか動作しない。

**解決策**:
1. インストールを確認:
   ```bash
   ls ComfyUI/custom_nodes/ComfyUI-Nudenet/
   ```

2. 依存関係を確認:
   ```bash
   pip install onnxruntime opencv-python pillow
   ```

3. ComfyUIを完全に再起動:
   ```bash
   # すべてのComfyUIプロセスを終了して再起動
   ```

#### モデル読み込みエラー

**問題**: モデルの読み込みに失敗するかメモリ不足エラーが発生する。

**解決策**:
1. 利用可能なVRAMを確認:
   ```bash
   nvidia-smi
   ```

2. より小さなモデルを使用するかCPUオフロードを有効化:
   ```bash
   python main.py --cpu
   ```

3. モデルファイルの整合性を確認:
   ```bash
   # 破損したモデルを再ダウンロード
   ```

### パフォーマンス最適化

#### GPUメモリ管理

1. **モデルオフロードを有効化**:
   ```bash
   python main.py --normalvram
   ```

2. **アテンション最適化を使用**:
   ```bash
   python main.py --use-split-cross-attention
   ```

#### NSFW検出最適化

1. **信頼度閾値を調整**:
   - 低い値: より敏感な検出
   - 高い値: 偽陽性が少ない

2. **検閲方法を最適化**:
   - ぼかし: 高速、ほとんどのコンテンツに適している
   - ピクセル化: より明確な検閲
   - オーバーレイ: カスタム画像オーバーレイ

## 高度な設定

### カスタムNSFWラベル

フィルタリングするコンテンツタイプを設定:

```python
# 設定内で
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

### ワークフローテンプレート

一般的な使用例のための再利用可能なワークフローテンプレートを作成:

1. **安全なポートレート生成**
2. **NSFWチェック付き風景**
3. **フィルタリング付き芸術的スタイル転送**
4. **安全性を考慮したバッチ処理**

### APIエンドポイント

システムは統合用のREST APIエンドポイントを提供:

```
POST /api/generate
POST /api/filter
GET /api/status
GET /api/models
```

### 監視とログ

デバッグ用の包括的なログを有効化:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## セキュリティ考慮事項

1. **APIセキュリティ**: APIアクセスに認証トークンを使用
2. **コンテンツログ**: 監査目的でフィルタリングされたコンテンツをログ
3. **ユーザー権限**: ロールベースのアクセス制御を実装
4. **データプライバシー**: 生成されたコンテンツを安全に処理

## 次のステップ

このセットアップを完了した後:

1. サンプルプロンプトで完全なパイプラインをテスト
2. 希望するチャットプラットフォームを設定
3. NSFWフィルタリングパラメータをカスタマイズ
4. 監視とログを設定
5. 本番環境にデプロイ

追加のヘルプについては、[API ドキュメント](API.ja.md)または[コントリビューションガイド](CONTRIBUTING.ja.md)を参照してください。
