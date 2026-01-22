from __future__ import annotations

import argparse
import sys
from pathlib import Path

from yt_audio_downloader.config import DownloadConfig
from yt_audio_downloader.downloader import DownloadError, download_audio
from yt_audio_downloader.logging_utils import setup_logging


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="yt-audio-downloader")
    p.add_argument("urls", nargs="+", help="One or more YouTube URLs")
    p.add_argument("-o", "--outdir", default="downloads", help="Output directory")
    p.add_argument("-f", "--format", default="mp3", help="Audio format (e.g., mp3)")
    p.add_argument("-q", "--quality", default="192K", help="Audio quality (e.g., 192K)")
    p.add_argument("--playlist", action="store_true", help="Allow playlist downloads")
    p.add_argument("-v", "--verbose", action="store_true", help="Verbose logging")
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    setup_logging(args.verbose)

    cfg = DownloadConfig(
        outdir=Path(args.outdir),
        audio_format=args.format,
        quality=args.quality,
        allow_playlist=args.playlist,
        verbose=args.verbose,
    )

    try:
        downloaded = download_audio(args.urls, cfg)
    except DownloadError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    for p in downloaded:
        print(p)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
