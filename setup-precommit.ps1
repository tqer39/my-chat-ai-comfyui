# Pre-commit setup script for Windows
# このスクリプトはpre-commitフックをセットアップします

param(
    [switch]$Force,
    [switch]$Help
)

# Color output functions
function Write-Success { param($Message) Write-Host $Message -ForegroundColor Green }
function Write-Warning { param($Message) Write-Host $Message -ForegroundColor Yellow }
function Write-Error { param($Message) Write-Host $Message -ForegroundColor Red }
function Write-Info { param($Message) Write-Host $Message -ForegroundColor Cyan }

# Help message
if ($Help) {
    Write-Info "=== Pre-commit Setup Script ==="
    Write-Info "このスクリプトはpre-commitフックをセットアップします。"
    Write-Info ""
    Write-Info "使用方法:"
    Write-Info "  .\setup-precommit.ps1          # 基本セットアップ"
    Write-Info "  .\setup-precommit.ps1 -Force   # 全ファイルでpre-commitを実行"
    Write-Info "  .\setup-precommit.ps1 -Help    # このヘルプを表示"
    Write-Info ""
    exit 0
}

Write-Info "=== Pre-commit Setup Script ==="
Write-Info "pre-commitフックをセットアップしています..."

# Check if we're in a git repository
try {
    git rev-parse --git-dir | Out-Null
    Write-Success "✓ Gitリポジトリが検出されました"
} catch {
    Write-Error "✗ Gitリポジトリではありません。Gitリポジトリ内で実行してください。"
    exit 1
}

# Install pre-commit if not already installed
try {
    pre-commit --version | Out-Null
    Write-Success "✓ pre-commitは既にインストールされています"
} catch {
    Write-Info "pre-commitをインストールしています..."
    try {
        # Try to use uv if available
        uv --version | Out-Null
        uv pip install pre-commit
        Write-Success "✓ pre-commitをuvでインストールしました"
    } catch {
        # Fallback to pip
        python -m pip install pre-commit
        Write-Success "✓ pre-commitをpipでインストールしました"
    }
}

# Install pre-commit hooks
Write-Info "pre-commitフックをインストールしています..."
try {
    pre-commit install
    Write-Success "✓ pre-commitフックがインストールされました"
} catch {
    Write-Error "✗ pre-commitフックのインストールに失敗しました"
    exit 1
}

# Run pre-commit on all files if Force flag is set
if ($Force) {
    Write-Info "全ファイルでpre-commitを実行しています..."
    try {
        pre-commit run --all-files
        Write-Success "✓ pre-commitの実行が完了しました"
    } catch {
        Write-Warning "⚠ pre-commitの実行中にエラーが発生しました（通常は修正可能な問題です）"
    }
}

Write-Success "✓ Pre-commitのセットアップが完了しました！"
Write-Info ""
Write-Info "次のステップ:"
Write-Info "1. コミット時に自動的にpre-commitが実行されます"
Write-Info "2. 手動実行: pre-commit run --all-files"
Write-Info "3. 特定ファイル: pre-commit run --files <ファイル名>"
Write-Info ""
