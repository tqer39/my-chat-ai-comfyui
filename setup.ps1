# ComfyUI NSFW Setup Script for Windows 11
# This script automates the installation and configuration of ComfyUI with NSFW filtering capabilities

param(
    [switch]$SkipComfyUI,
    [switch]$SkipPython,
    [switch]$SkipModels,
    [string]$InstallPath = "C:\ComfyUI",
    [string]$PythonVersion = "3.11"
)

# Script configuration
$ErrorActionPreference = "Stop"
$ProgressPreference = "Continue"

# Color output functions
function Write-Success { param($Message) Write-Host $Message -ForegroundColor Green }
function Write-Warning { param($Message) Write-Host $Message -ForegroundColor Yellow }
function Write-Error { param($Message) Write-Host $Message -ForegroundColor Red }
function Write-Info { param($Message) Write-Host $Message -ForegroundColor Cyan }

# Main setup function
function Main {
    Write-Info "=== ComfyUI NSFW Setup Script for Windows 11 ==="
    Write-Info "This script will install and configure:"
    Write-Info "- Python $PythonVersion"
    Write-Info "- ComfyUI with GPU support"
    Write-Info "- ComfyUI-Nudenet extension"
    Write-Info "- My-Chat-AI-ComfyUI integration"
    Write-Info ""

    # Check if running as administrator
    if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
        Write-Error "This script requires administrator privileges. Please run as administrator."
        exit 1
    }

    # System requirements check
    Test-SystemRequirements

    # Installation steps
    if (-not $SkipPython) { Install-Python }
    if (-not $SkipComfyUI) { Install-ComfyUI }
    Install-ComfyUINudenet
    Install-ChatAIIntegration
    if (-not $SkipModels) { Download-Models }
    Configure-Environment
    Test-Installation

    Write-Success "=== Setup completed successfully! ==="
    Write-Info "Next steps:"
    Write-Info "1. Start ComfyUI: cd $InstallPath && .\run_nvidia_gpu.bat"
    Write-Info "2. Open browser: http://localhost:8188"
    Write-Info "3. Start chat AI service: python src\main.py"
    Write-Info ""
    Write-Info "For detailed usage instructions, see docs\HOWTO.md"
}

# Check system requirements
function Test-SystemRequirements {
    Write-Info "Checking system requirements..."

    # Check Windows version
    $osVersion = [System.Environment]::OSVersion.Version
    if ($osVersion.Major -lt 10) {
        Write-Error "Windows 10 or higher is required"
        exit 1
    }
    Write-Success "✓ Windows version check passed"

    # Check available disk space (50GB minimum)
    $freeSpace = (Get-WmiObject -Class Win32_LogicalDisk -Filter "DeviceID='C:'").FreeSpace / 1GB
    if ($freeSpace -lt 50) {
        Write-Warning "⚠ Low disk space: ${freeSpace}GB available. 50GB recommended."
    } else {
        Write-Success "✓ Disk space check passed: ${freeSpace}GB available"
    }

    # Check RAM (16GB recommended)
    $totalRAM = (Get-WmiObject -Class Win32_ComputerSystem).TotalPhysicalMemory / 1GB
    if ($totalRAM -lt 16) {
        Write-Warning "⚠ Low RAM: ${totalRAM}GB detected. 16GB recommended for optimal performance."
    } else {
        Write-Success "✓ RAM check passed: ${totalRAM}GB available"
    }

    # Check for NVIDIA GPU
    try {
        $gpu = Get-WmiObject -Class Win32_VideoController | Where-Object { $_.Name -like "*NVIDIA*" }
        if ($gpu) {
            Write-Success "✓ NVIDIA GPU detected: $($gpu.Name)"
        } else {
            Write-Warning "⚠ No NVIDIA GPU detected. CPU-only mode will be used."
        }
    } catch {
        Write-Warning "⚠ Could not detect GPU information"
    }

    # Check for Git
    try {
        $gitVersion = git --version
        Write-Success "✓ Git is installed: $gitVersion"
    } catch {
        Write-Error "Git is required but not installed. Please install Git first."
        Write-Info "Download from: https://git-scm.com/download/win"
        exit 1
    }
}

# Install Python via scoop and uv
function Install-Python {
    Write-Info "Installing Python via scoop and uv..."

    # Check if scoop is installed
    try {
        scoop --version | Out-Null
        Write-Success "✓ Scoop is already installed"
    } catch {
        Write-Info "Installing Scoop..."
        Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
        Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression

        # Refresh PATH to include scoop
        $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "User") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "Machine")
    }

    # Install uv via scoop
    try {
        uv --version | Out-Null
        Write-Success "✓ uv is already installed"
    } catch {
        Write-Info "Installing uv via scoop..."
        scoop install main/uv

        # Refresh PATH to include uv
        $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "User") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "Machine")
    }

    # Install Python via uv
    Write-Info "Installing Python $PythonVersion via uv..."
    uv python install $PythonVersion
    uv python pin $PythonVersion

    # Verify installation
    try {
        $pythonVersion = uv run python --version
        Write-Success "✓ Python installed successfully via uv: $pythonVersion"
    } catch {
        Write-Error "Python installation via uv failed. Please check the installation."
        exit 1
    }
}

# Install ComfyUI
function Install-ComfyUI {
    Write-Info "Installing ComfyUI..."

    # Create installation directory
    if (-not (Test-Path $InstallPath)) {
        New-Item -ItemType Directory -Path $InstallPath -Force | Out-Null
        Write-Success "✓ Created installation directory: $InstallPath"
    }

    # Check if ComfyUI is already installed
    if (Test-Path "$InstallPath\main.py") {
        Write-Success "✓ ComfyUI is already installed"
        return
    }

    # Clone ComfyUI repository
    Write-Info "Cloning ComfyUI repository..."
    Set-Location $InstallPath
    git clone https://github.com/comfyanonymous/ComfyUI.git .

    # Install Python dependencies
    Write-Info "Installing ComfyUI dependencies..."
    uv pip install --upgrade pip

    # Install PyTorch with CUDA support
    Write-Info "Installing PyTorch with CUDA support..."
    uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

    # Install other requirements
    if (Test-Path "requirements.txt") {
        uv pip install -r requirements.txt
    }

    Write-Success "✓ ComfyUI installed successfully"
}

# Install ComfyUI-Nudenet extension
function Install-ComfyUINudenet {
    Write-Info "Installing ComfyUI-Nudenet extension..."

    $customNodesPath = "$InstallPath\custom_nodes"
    $nudenetPath = "$customNodesPath\ComfyUI-Nudenet"

    # Create custom_nodes directory if it doesn't exist
    if (-not (Test-Path $customNodesPath)) {
        New-Item -ItemType Directory -Path $customNodesPath -Force | Out-Null
    }

    # Check if already installed
    if (Test-Path $nudenetPath) {
        Write-Success "✓ ComfyUI-Nudenet is already installed"
        return
    }

    # Clone the extension
    Set-Location $customNodesPath
    git clone https://github.com/phuvinh010701/ComfyUI-Nudenet.git

    # Install extension dependencies
    Set-Location $nudenetPath
    if (Test-Path "requirements.txt") {
        uv pip install -r requirements.txt
    }

    # Install additional dependencies
    uv pip install onnxruntime opencv-python pillow

    Write-Success "✓ ComfyUI-Nudenet extension installed successfully"
}

# Install Chat AI Integration
function Install-ChatAIIntegration {
    Write-Info "Installing Chat AI Integration components..."

    # Return to project root
    Set-Location (Split-Path -Parent $PSScriptRoot)

    # Install project dependencies
    if (Test-Path "requirements.txt") {
        Write-Info "Installing project dependencies..."
        uv pip install -r requirements.txt
    }

    # Create necessary directories
    $directories = @("src", "config", "logs", "temp")
    foreach ($dir in $directories) {
        if (-not (Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
            Write-Success "✓ Created directory: $dir"
        }
    }

    # Copy example configuration
    if ((Test-Path "config\example.env") -and (-not (Test-Path ".env"))) {
        Copy-Item "config\example.env" ".env"
        Write-Success "✓ Created .env configuration file"
        Write-Warning "⚠ Please edit .env file with your API keys and configuration"
    }

    Write-Success "✓ Chat AI Integration components installed"
}

# Download essential models
function Download-Models {
    Write-Info "Downloading essential models..."

    $modelsPath = "$InstallPath\models"
    $checkpointsPath = "$modelsPath\checkpoints"

    # Create models directories
    $modelDirs = @("checkpoints", "vae", "loras", "controlnet", "Nudenet")
    foreach ($dir in $modelDirs) {
        $dirPath = "$modelsPath\$dir"
        if (-not (Test-Path $dirPath)) {
            New-Item -ItemType Directory -Path $dirPath -Force | Out-Null
        }
    }

    # Download Stable Diffusion 3.5 Medium (manual download required)
    $sd35Path = "$checkpointsPath\sd3.5_medium.safetensors"
    if (-not (Test-Path $sd35Path)) {
        Write-Warning "⚠ Stable Diffusion 3.5 Medium requires manual download due to license requirements."
        Write-Info "Please follow these steps:"
        Write-Info "1. Visit: https://huggingface.co/stabilityai/stable-diffusion-3.5-medium"
        Write-Info "2. Accept the license terms"
        Write-Info "3. Download sd3.5_medium.safetensors"
        Write-Info "4. Place the file in: $sd35Path"
        Write-Info ""
        Write-Info "The system will work with any compatible SD3.5 Medium model file."
    } else {
        Write-Success "✓ Stable Diffusion 3.5 Medium model found"
    }

    Write-Info "Note: NSFW detection model will be downloaded automatically on first use"
}

# Configure environment
function Configure-Environment {
    Write-Info "Configuring environment..."

    # Create batch files for easy startup
    $runBatContent = @"
@echo off
cd /d "$InstallPath"
python main.py --listen 0.0.0.0 --port 8188
pause
"@

    $runBatPath = "$InstallPath\run_comfyui.bat"
    $runBatContent | Out-File -FilePath $runBatPath -Encoding ASCII
    Write-Success "✓ Created startup script: $runBatPath"

    # Create desktop shortcut
    try {
        $WshShell = New-Object -comObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\ComfyUI.lnk")
        $Shortcut.TargetPath = $runBatPath
        $Shortcut.WorkingDirectory = $InstallPath
        $Shortcut.Description = "ComfyUI with NSFW Filtering"
        $Shortcut.Save()
        Write-Success "✓ Created desktop shortcut"
    } catch {
        Write-Warning "⚠ Could not create desktop shortcut"
    }

    # Set up Windows Firewall rule (optional)
    try {
        $firewallRule = Get-NetFirewallRule -DisplayName "ComfyUI" -ErrorAction SilentlyContinue
        if (-not $firewallRule) {
            New-NetFirewallRule -DisplayName "ComfyUI" -Direction Inbound -Protocol TCP -LocalPort 8188 -Action Allow | Out-Null
            Write-Success "✓ Added Windows Firewall rule for ComfyUI"
        }
    } catch {
        Write-Warning "⚠ Could not configure Windows Firewall rule"
    }
}

# Test installation
function Test-Installation {
    Write-Info "Testing installation..."

    # Test Python imports
    try {
        python -c "import torch; print(f'PyTorch version: {torch.__version__}')"
        Write-Success "✓ PyTorch import test passed"
    } catch {
        Write-Error "✗ PyTorch import test failed"
    }

    try {
        python -c "import cv2; print(f'OpenCV version: {cv2.__version__}')"
        Write-Success "✓ OpenCV import test passed"
    } catch {
        Write-Warning "⚠ OpenCV import test failed"
    }

    # Test ComfyUI structure
    $requiredFiles = @("main.py", "server.py", "execution.py")
    foreach ($file in $requiredFiles) {
        if (Test-Path "$InstallPath\$file") {
            Write-Success "✓ Found required file: $file"
        } else {
            Write-Error "✗ Missing required file: $file"
        }
    }

    # Test Nudenet extension
    if (Test-Path "$InstallPath\custom_nodes\ComfyUI-Nudenet\__init__.py") {
        Write-Success "✓ ComfyUI-Nudenet extension found"
    } else {
        Write-Error "✗ ComfyUI-Nudenet extension not found"
    }

    Write-Info "Installation test completed"
}

# Error handling
trap {
    Write-Error "An error occurred during setup: $_"
    Write-Info "Please check the error message above and try again."
    Write-Info "For help, see the documentation at docs\HOWTO.md"
    exit 1
}

# Run main function
Main
