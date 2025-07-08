cd python
uv run convert-output
uv run startup
cd ..
.\bonsai\Bonsai.exe .\src\SoundLateralizationTask.bonsai --start
cd python
uv run convert-output