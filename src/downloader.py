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
    # Saída com nome do título e ID para reduzir colisões
    outtmpl = str(cfg.outdir / "%(title).200s [%(id)s].%(ext)s")

    postprocessors = [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": cfg.audio_format,
            "preferredquality": cfg.quality.replace("K", ""),  # yt-dlp espera numérico p/ mp3
        }
    ]

    return {
        "format": "bestaudio/best",
        "outtmpl": outtmpl,
        "noplaylist": not cfg.allow_playlist,
        "quiet": not cfg.verbose,
        "no_warnings": not cfg.verbose,
        "postprocessors": postprocessors,
        # Evitar problemas de caracteres inválidos em nomes de arquivo (Windows principalmente)
        "restrictfilenames": False,
        # Recomendável para consistência
        "paths": {"home": str(cfg.outdir)},
    }


def download_audio(urls: Iterable[str], cfg: DownloadConfig) -> list[Path]:
    """
    Baixa áudio de uma lista de URLs. Retorna paths previstos dos arquivos.
    Observação: o yt-dlp pode ajustar extensões ao final, mas aqui retornamos um "best effort".
    """
    cfg.ensure_outdir()

    ydl_opts = _build_ydl_opts(cfg)
    downloaded: list[Path] = []

    log.info("Starting download: %d URL(s)", len(list(urls)) if not isinstance(urls, list) else len(urls))

    # Para não consumir iteráveis duas vezes, normaliza:
    url_list = list(urls)

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url_list, download=True)

            # info pode ser dict (single) ou dict com entries (playlist)
            entries = []
            if isinstance(info, dict) and "entries" in info and info["entries"] is not None:
                entries = [e for e in info["entries"] if e is not None]
            elif isinstance(info, dict):
                entries = [info]

            # "best effort" de paths finais:
            for e in entries:
                title = (e.get("title") or "audio").strip()
                vid = (e.get("id") or "unknown").strip()
                # após postprocess, extensão vira cfg.audio_format
                filename = f"{title} [{vid}].{cfg.audio_format}"
                downloaded.append(cfg.outdir / filename)

    except Exception as exc:  # yt-dlp levanta várias exceções internas
        raise DownloadError(str(exc)) from exc

    return downloaded
