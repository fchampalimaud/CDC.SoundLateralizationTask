if (!(Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "Installing uv ..."
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
}

cd .\bonsai

if (!(Test-Path "./Bonsai.exe")) {
    Invoke-WebRequest "https://github.com/bonsai-rx/bonsai/releases/download/2.8.2/Bonsai.zip" -OutFile "temp.zip"
    Move-Item -Path "NuGet.config" "temp.config"
    Expand-Archive "temp.zip" -DestinationPath "." -Force
    Move-Item -Path "temp.config" "NuGet.config" -Force
    Remove-Item -Path "temp.zip"
    Remove-Item -Path "Bonsai32.exe"
}
& .\Bonsai.exe --no-editor

cd ..

# Checks if the output directory already exists
if (!(Test-Path ".\config")) { 
    New-Item -ItemType Directory -Path "config" 
}

# Define repository owner and name
$repoOwner = "fchampalimaud"
$repoName = "CDC.SoundLateralizationTask"
$assetName = "template.yml"  # Replace with the name of the specific file you want to download

# Get the latest release information
$apiUrl = "https://api.github.com/repos/$repoOwner/$repoName/releases/latest"
$releaseInfo = Invoke-RestMethod -Uri $apiUrl

# Find the specific asset
$asset = $releaseInfo.assets | Where-Object { $_.name -eq $assetName }

if ($asset) {
    # Get the URL of the specific asset
    $assetUrl = $asset.browser_download_url

    # Check if the file already exists
    $outputFile = "config/template.yml"
    if (-Not (Test-Path -Path $outputFile)) {
        # Download the specific asset
        Invoke-WebRequest -Uri $assetUrl -OutFile $outputFile
        Write-Output "Downloaded $assetName to $outputFile"
    } else {
        Write-Output "$assetName already exists. Skipping download."
    }
} else {
    Write-Output "Asset $assetName not found in the latest release."
}

$assetName = "setup.csv"  # Replace with the name of the specific file you want to download

# Get the latest release information
$apiUrl = "https://api.github.com/repos/$repoOwner/$repoName/releases/latest"
$releaseInfo = Invoke-RestMethod -Uri $apiUrl

# Find the specific asset
$asset = $releaseInfo.assets | Where-Object { $_.name -eq $assetName }

if ($asset) {
    # Get the URL of the specific asset
    $assetUrl = $asset.browser_download_url

    # Check if the file already exists
    $outputFile = "config/$assetName"
    if (-Not (Test-Path -Path $outputFile)) {
        # Download the specific asset
        Invoke-WebRequest -Uri $assetUrl -OutFile $outputFile
        Write-Output "Downloaded $assetName to $outputFile"
    } else {
        Write-Output "$assetName already exists. Skipping download."
    }
} else {
    Write-Output "Asset $assetName not found in the latest release."
}

$assetName = "training.csv"  # Replace with the name of the specific file you want to download

# Get the latest release information
$apiUrl = "https://api.github.com/repos/$repoOwner/$repoName/releases/latest"
$releaseInfo = Invoke-RestMethod -Uri $apiUrl

# Find the specific asset
$asset = $releaseInfo.assets | Where-Object { $_.name -eq $assetName }

if ($asset) {
    # Get the URL of the specific asset
    $assetUrl = $asset.browser_download_url

    # Check if the file already exists
    $outputFile = "config/$assetName"
    if (-Not (Test-Path -Path $outputFile)) {
        # Download the specific asset
        Invoke-WebRequest -Uri $assetUrl -OutFile $outputFile
        Write-Output "Downloaded $assetName to $outputFile"
    } else {
        Write-Output "$assetName already exists. Skipping download."
    }
} else {
    Write-Output "Asset $assetName not found in the latest release."
}

if (!(Test-Path ".\assets\toSoundCard.exe")) {
    Invoke-WebRequest "https://github.com/fchampalimaud/cdc-speaker-calibration/releases/download/v0.3.0-alpha/toSoundCard.exe" -OutFile ".\python\assets\toSoundCard.exe"
}

if (!(Test-Path ".\assets\LibUsbDotNet.dll")) {
    Invoke-WebRequest "https://github.com/fchampalimaud/cdc-speaker-calibration/releases/download/v0.3.0-alpha/LibUsbDotNet.dll" -OutFile ".\python\assets\LibUsbDotNet.dll"
}

cd .\python
uv run config