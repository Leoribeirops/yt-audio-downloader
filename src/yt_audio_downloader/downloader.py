from __future__ import annotations

import logging
from pathlib import Path
from typing import Iterable

from yt_dlp import YoutubeDL

from .config import DownloadConfig

log = logging.getLogger(__name__)


class DownloadError(RuntimeError):
    pass


def _build_ydl_opts(cfg: DownloadConfig) -> dict:
    outtmpl = str(cfg.outdir / "%(title).200s [%(id)s].%(ext)s")

    postprocessors = [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": cfg.audio_format,
            "preferredquality": cfg.quality.replace("K", ""),
        }
    ]

    return {
        "format": "bestaudio/best",
        "outtmpl": outtmpl,
        "noplaylist": not cfg.allow_playlist,
        "quiet": not cfg.verbose,
        "no_warnings": not cfg.verbose,
        "postprocessors": postprocessors,
        "restrictfilenames": False,
        "paths": {"home": str(cfg.outdir)},
    }


def download_audio(urls: Iterable[str], cfg: DownloadConfig) -> list[Path]:
    """
    Baixa áudio de uma lista de URLs. Retorna paths previstos dos arquivos.
    Observação: o yt-dlp pode ajustar extensões ao final, mas aqui retornamos um "best effort".
    """
    cfg.ensure_outdir()

    # Normaliza UMA vez (não consome iterável duas vezes)
    url_list = list(urls)

    # Validação defensiva (evita erros obscuros)
    for u in url_list:
        if not isinstance(u, str):
            raise TypeError(f"Each URL must be a str, got {type(u).__name__}: {u!r}")
        if not u.strip():
            raise ValueError("Empty URL provided")

    log.info("Starting download: %d URL(s)", len(url_list))

    ydl_opts = _build_ydl_opts(cfg)
    downloaded: list[Path] = []

    try:
        with YoutubeDL(ydl_opts) as ydl:
            for url in url_list:
                info = ydl.extract_info(url, download=True)

                # info pode ser dict (single) ou dict com entries (playlist)
                if isinstance(info, dict) and info.get("entries"):
                    entries = [e for e in info["entries"] if e is not None]
                else:
                    entries = [info] if isinstance(info, dict) else []

                for e in entries:
                    title = (e.get("title") or "audio").strip()
                    vid = (e.get("id") or "unknown").strip()
                    filename = f"{title} [{vid}].{cfg.audio_format}"
                    downloaded.append(cfg.outdir / filename)

    except Exception as exc:
        raise DownloadError(str(exc)) from exc

    return downloaded
