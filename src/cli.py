from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .config import DownloadConfig
from .downloader import DownloadError, download_audio
from .logging_utils import setup_logging


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="yt-audio-downloader",
        description="Download audio from YouTube URLs (via yt-dlp).",
    )
    p.add_argument("urls", nargs="+", help="One or more YouTube URLs.")
    p.add_argument("--outdir", default="downloads", help="Output directory (default: downloads).")
    p.add_argument(
        "--format",
        default="mp3",
        dest="audio_format",
        help="Audio format (e.g., mp3, m4a, opus). Default: mp3.",
    )
    p.add_argument(
        "--quality",
        default="192K",
        help="Audio quality hint (mainly for mp3). Default: 192K.",
    )
    p.add_argument(
        "--playlist",
        action="store_true",
        help="Allow playlist downloads (default: disabled).",
    )
    p.add_argument("--verbose", action="store_true", help="Verbose logging.")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    cfg = DownloadConfig(
        outdir=Path(args.outdir),
        audio_format=args.audio_format,
        quality=args.quality,
        allow_playlist=args.playlist,
        verbose=args.verbose,
    )
    setup_logging(cfg.verbose)

    try:
        paths = download_audio(args.urls, cfg)
    except DownloadError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    # Saída amigável para scripts
    for p in paths:
        print(p)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
