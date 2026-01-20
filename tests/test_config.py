from __future__ import annotations

from pathlib import Path

from yt_audio_downloader.config import DownloadConfig


def test_ensure_outdir_creates_dir(tmp_path: Path) -> None:
    out = tmp_path / "x" / "y"
    cfg = DownloadConfig(outdir=out)
    cfg.ensure_outdir()
    assert out.exists()
    assert out.is_dir()
