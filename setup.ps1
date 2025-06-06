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

cd ..\python

uv run config