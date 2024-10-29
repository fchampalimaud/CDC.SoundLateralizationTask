if (!(Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Poetry using pipx..."
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
}

cd .\bonsai
.\setup.ps1