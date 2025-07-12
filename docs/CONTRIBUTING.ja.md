# コントリビューションガイド

My Chat AI ComfyUIプロジェクトへのコントリビューションを歓迎します！このガイドでは、プロジェクトに貢献する方法について説明します。

## 目次

1. [行動規範](#行動規範)
2. [コントリビューターの前提条件](#コントリビューターの前提条件)
3. [開発環境のセットアップ](#開発環境のセットアップ)
4. [コントリビューションプロセス](#コントリビューションプロセス)
5. [コードスタイル](#コードスタイル)
6. [テスト](#テスト)
7. [ドキュメント](#ドキュメント)
8. [コミュニティ](#コミュニティ)

## 行動規範

### 私たちの約束

私たちは、年齢、体型、障害の有無、民族性、性的特徴、性自認と表現、経験レベル、教育、社会経済的地位、国籍、外見、人種、宗教、性的指向に関係なく、すべての人にとってハラスメントのない環境を提供することを約束します。

### 私たちの基準

ポジティブな環境を作り出すための行動例：

- 他者に対する共感と親切さを示す
- 異なる意見、視点、経験を尊重する
- 建設的なフィードバックを与え、優雅に受け入れる
- 間違いを認め、影響を受けた人々に謝罪し、経験から学ぶ
- 個人だけでなく、コミュニティ全体にとって最善のことに焦点を当てる

受け入れられない行動例：

- 性的な言葉や画像の使用、および性的な注意や進歩
- トローリング、侮辱的または軽蔑的なコメント、個人的または政治的攻撃
- 公的または私的なハラスメント
- 明示的な許可なしに他者の個人情報（住所や電子メールアドレスなど）を公開すること
- 職業的環境で合理的に不適切と考えられるその他の行為

## コントリビューターの前提条件

### 技術的要件

- **Python**: 3.8以上
- **Git**: バージョン管理の基本的な知識
- **GitHub**: プルリクエストとイシューの作成経験
- **ComfyUI**: 基本的な理解（推奨）
- **AI/ML**: 機械学習の基本概念（推奨）

### 推奨スキル

- **自然言語処理**: テキスト処理とインテント認識
- **API設計**: RESTfulサービスとWebSocket
- **チャットボット開発**: Discord、Slack、Telegram統合
- **画像処理**: Stable Diffusion、ComfyUIワークフロー
- **テスト駆動開発**: pytest、モッキング、統合テスト

## 開発環境のセットアップ

### 1. リポジトリのフォークとクローン

```bash
# GitHubでリポジトリをフォーク
# フォークしたリポジトリをクローン
git clone https://github.com/YOUR_USERNAME/my-chat-ai-comfyui.git
cd my-chat-ai-comfyui

# オリジナルリポジトリをupstreamとして追加
git remote add upstream https://github.com/tqer39/my-chat-ai-comfyui.git
```

### 2. Python環境のセットアップ

```bash
# Python仮想環境を作成
python -m venv venv

# 仮想環境を有効化
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 依存関係をインストール
pip install -e ".[dev]"
```

### 3. pre-commitフックのセットアップ

```bash
# pre-commitをインストール
pre-commit install

# すべてのファイルでフックを実行（初回）
pre-commit run --all-files
```

### 4. 環境設定

```bash
# 設定ファイルをコピー
cp config/example.env .env

# 必要に応じて.envファイルを編集
# テスト用のAPIキーやトークンを設定
```

### 5. ComfyUIのセットアップ（オプション）

```bash
# ComfyUIをセットアップ（統合テスト用）
python setup.py install_comfyui
```

## コントリビューションプロセス

### 1. イシューの確認

- 既存のイシューを確認し、重複を避ける
- 新しい機能や大きな変更の場合は、まずイシューを作成して議論する
- 「good first issue」ラベルの付いたイシューは初心者におすすめ

### 2. ブランチの作成

```bash
# 最新のmainブランチを取得
git checkout main
git pull upstream main

# 新しいブランチを作成
git checkout -b feature/your-feature-name
# または
git checkout -b fix/issue-number-description
```

### 3. 開発

- 小さく、論理的なコミットを作成
- コミットメッセージは明確で説明的に
- テストを追加または更新
- ドキュメントを更新

### 4. テストの実行

```bash
# 単体テストを実行
pytest tests/

# 統合テストを実行（ComfyUIが必要）
pytest tests/ -m integration

# カバレッジレポートを生成
pytest --cov=src tests/

# リンターとフォーマッターを実行
ruff check src/ tests/
ruff format src/ tests/
mypy src/
```

### 5. プルリクエストの作成

```bash
# 変更をプッシュ
git push origin feature/your-feature-name
```

GitHubでプルリクエストを作成し、以下を含める：

- **明確なタイトル**: 変更内容を簡潔に説明
- **詳細な説明**: 何を変更し、なぜ変更したかを説明
- **関連イシュー**: `Fixes #123`または`Closes #123`
- **テスト結果**: テストが通ることを確認
- **スクリーンショット**: UI変更がある場合

### 6. レビューと修正

- レビュアーからのフィードバックに対応
- 必要に応じて追加のコミットを作成
- CIチェックが通ることを確認

## コードスタイル

### Python コードスタイル

プロジェクトでは以下のツールを使用：

- **Ruff**: リンティングとフォーマッティング
- **mypy**: 型チェック
- **Black**: コードフォーマッティング（Ruffに統合）

### スタイルガイドライン

```python
# 良い例
def process_chat_message(
    message: str,
    user_id: str,
    options: Optional[Dict[str, Any]] = None
) -> ChatResponse:
    """チャットメッセージを処理し、ComfyUIワークフローを生成する。

    Args:
        message: ユーザーからのメッセージ
        user_id: ユーザーID
        options: オプション設定

    Returns:
        処理結果を含むChatResponse

    Raises:
        InvalidMessageError: メッセージが無効な場合
    """
    if not message.strip():
        raise InvalidMessageError("メッセージが空です")

    # 処理ロジック
    return ChatResponse(success=True, data=result)
```

### 命名規則

- **関数・変数**: `snake_case`
- **クラス**: `PascalCase`
- **定数**: `UPPER_SNAKE_CASE`
- **プライベートメンバー**: `_leading_underscore`

### インポート順序

```python
# 標準ライブラリ
import json
import logging
from typing import Dict, List, Optional

# サードパーティライブラリ
import requests
from fastapi import FastAPI

# ローカルインポート
from src.chat_interface import ChatManager
from src.comfyui_control import ComfyUIClient
```

## テスト

### テスト構造

```text
tests/
├── unit/                   # 単体テスト
│   ├── test_chat_manager.py
│   ├── test_intent_processor.py
│   └── test_workflow_orchestrator.py
├── integration/            # 統合テスト
│   ├── test_api_endpoints.py
│   └── test_comfyui_integration.py
├── fixtures/               # テストデータ
│   ├── sample_workflows.json
│   └── mock_responses.json
└── conftest.py            # pytest設定
```

### テストの書き方

```python
import pytest
from unittest.mock import Mock, patch

from src.chat_interface import ChatManager


class TestChatManager:
    @pytest.fixture
    def chat_manager(self):
        return ChatManager(api_key="test_key")

    @pytest.fixture
    def mock_comfyui_client(self):
        client = Mock()
        client.queue_prompt.return_value = "prompt_123"
        return client

    def test_process_message_success(self, chat_manager, mock_comfyui_client):
        # Arrange
        message = "美しい風景を生成してください"
        chat_manager.comfyui_client = mock_comfyui_client

        # Act
        result = chat_manager.process_message(message, "user_123")

        # Assert
        assert result.success is True
        assert result.prompt_id == "prompt_123"
        mock_comfyui_client.queue_prompt.assert_called_once()

    @pytest.mark.asyncio
    async def test_async_processing(self, chat_manager):
        # 非同期テストの例
        result = await chat_manager.process_async("test message")
        assert result is not None

    @pytest.mark.integration
    def test_full_pipeline(self):
        # 統合テスト（実際のComfyUIが必要）
        pass
```

### テストの実行

```bash
# すべてのテストを実行
pytest

# 特定のテストファイルを実行
pytest tests/unit/test_chat_manager.py

# 特定のテストメソッドを実行
pytest tests/unit/test_chat_manager.py::TestChatManager::test_process_message_success

# 統合テストを除外
pytest -m "not integration"

# カバレッジレポート付きで実行
pytest --cov=src --cov-report=html
```

## ドキュメント

### ドキュメント構造

```text
docs/
├── README.ja.md           # プロジェクト概要（日本語）
├── HOWTO.ja.md           # セットアップガイド（日本語）
├── API.ja.md             # API仕様書（日本語）
├── CONTRIBUTING.ja.md    # このファイル
└── examples/             # 使用例
    ├── basic_usage.py
    ├── discord_bot.py
    └── custom_workflow.py
```

### ドキュメントの更新

- 新機能を追加した場合は、対応するドキュメントを更新
- APIの変更がある場合は、API.ja.mdを更新
- 使用例やチュートリアルを追加する場合は、examples/に配置

### ドキュメントのスタイル

- 明確で簡潔な説明
- コード例を含める
- 日本語と英語の両方を維持
- マークダウンの標準的な書式を使用

## コミュニティ

### コミュニケーション

- **GitHub Issues**: バグレポート、機能リクエスト
- **GitHub Discussions**: 一般的な議論、質問、アイデア共有
- **Discord**: リアルタイムチャット、コミュニティサポート
- **メール**: プライベートな問い合わせ

### 貢献の認識

コントリビューターの貢献を以下の方法で認識します：

- **Contributors.md**: すべてのコントリビューターをリストアップ
- **リリースノート**: 主要な貢献を特記
- **GitHub Achievements**: 貢献に応じたバッジとアチーブメント
- **コミュニティスポットライト**: 月次のコントリビューター紹介

### イベントと活動

- **月次コミュニティミーティング**: プロジェクトの進捗と議論
- **ハッカソン**: 新機能の開発とアイデア実装
- **ワークショップ**: 技術的なトピックの学習セッション
- **コードレビューセッション**: ベストプラクティスの共有

## 質問とサポート

### よくある質問

**Q: 初心者でも貢献できますか？**
A: はい！「good first issue」ラベルの付いたイシューから始めることをお勧めします。

**Q: どのような種類の貢献が歓迎されますか？**
A: コード、ドキュメント、テスト、バグレポート、機能提案、翻訳など、すべての貢献を歓迎します。

**Q: プルリクエストのレビューにはどのくらい時間がかかりますか？**
A: 通常、1-3営業日以内にレビューを行います。複雑な変更の場合はより長くかかる場合があります。

### サポートリソース

- **ドキュメント**: [docs/](../docs/)
- **API リファレンス**: [API.ja.md](API.ja.md)
- **セットアップガイド**: [HOWTO.ja.md](HOWTO.ja.md)
- **GitHub Issues**: バグレポートと機能リクエスト
- **Discord コミュニティ**: リアルタイムサポート

## ライセンスと著作権

このプロジェクトにコントリビューションすることで、あなたの貢献がプロジェクトと同じライセンス（MIT License）の下でライセンスされることに同意したものとみなされます。

---

My Chat AI ComfyUIプロジェクトへのコントリビューションをありがとうございます！あなたの貢献がコミュニティ全体の成長と発展に役立ちます。
