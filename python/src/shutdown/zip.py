import shutil
import zipfile
from pathlib import Path


def zip_events(dir: Path):
    events_dir = dir / "events"

    with zipfile.ZipFile(
        dir / "events.zip", "w", compression=zipfile.ZIP_DEFLATED
    ) as zf:
        for path in events_dir.rglob("*"):
            if path.is_file():
                zf.write(path)

    shutil.rmtree(events_dir)
