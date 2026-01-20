from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DownloadConfig:
    outdir: Path
    audio_format: str = "mp3"
    quality: str = "192K"
    allow_playlist: bool = False
    verbose: bool = False

    def ensure_outdir(self) -> None:
        self.outdir.mkdir(parents=True, exist_ok=True)
