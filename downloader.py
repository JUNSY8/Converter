"""Song search and download engine powered by yt-dlp."""

from __future__ import annotations

import re
import shutil
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import yt_dlp

ProgressCallback = Callable[[str], None]
ItemDoneCallback = Callable[[int, int, str, bool, str], None]


@dataclass(frozen=True)
class SongQuery:
    title: str
    artist: str = ""

    @property
    def search_query(self) -> str:
        parts = [p for p in (self.title, self.artist) if p]
        return " ".join(parts)

    @property
    def display_name(self) -> str:
        if self.artist:
            return f"{self.artist} - {self.title}"
        return self.title


AUDIO_QUALITIES = ("128", "192", "320")
VIDEO_QUALITIES = ("360", "720", "1080")


def ffmpeg_available() -> bool:
    return shutil.which("ffmpeg") is not None


def sanitize_filename(name: str) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", name).strip(" .")
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned or "sin_titulo"


def parse_song_line(line: str) -> SongQuery | None:
    text = line.strip()
    if not text or text.startswith("#"):
        return None

    for separator in (" - ", " – ", " — ", ", "):
        if separator in text:
            left, right = text.split(separator, 1)
            left, right = left.strip(), right.strip()
            if left and right:
                return SongQuery(title=left, artist=right)

    return SongQuery(title=text)


def parse_song_list(text: str) -> list[SongQuery]:
    songs: list[SongQuery] = []
    for line in text.splitlines():
        song = parse_song_line(line)
        if song:
            songs.append(song)
    return songs


def _build_ydl_opts(
    output_path_no_ext: Path,
    file_format: str,
    quality: str,
    progress_hook: Callable[[dict], None] | None = None,
) -> dict:
    opts: dict = {
        "outtmpl": str(output_path_no_ext) + ".%(ext)s",
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "ignoreerrors": False,
        "windowsfilenames": True,
        "overwrites": True,
    }

    if progress_hook is not None:
        opts["progress_hooks"] = [progress_hook]

    if file_format.lower() == "mp3":
        opts.update(
            {
                "format": "bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": quality,
                    },
                    {"key": "FFmpegMetadata"},
                ],
            }
        )
    else:
        height = quality if quality.isdigit() else "720"
        opts.update(
            {
                "format": (
                    f"bestvideo[height<={height}][ext=mp4]+bestaudio[ext=m4a]"
                    f"/bestvideo[height<={height}]+bestaudio"
                    f"/best[height<={height}]/best"
                ),
                "merge_output_format": "mp4",
                "postprocessors": [{"key": "FFmpegMetadata"}],
            }
        )

    return opts


def download_song(
    song: SongQuery,
    output_dir: Path,
    file_format: str,
    quality: str,
    on_log: ProgressCallback | None = None,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    base_name = sanitize_filename(song.display_name)
    output_stem = output_dir / base_name
    expected_ext = "mp3" if file_format.lower() == "mp3" else "mp4"
    expected = output_stem.with_suffix(f".{expected_ext}")

    def hook(status: dict) -> None:
        if status.get("status") == "finished" and on_log:
            on_log(f"Procesando: {song.display_name}")
        elif status.get("status") == "downloading" and on_log:
            percent = status.get("_percent_str", "").strip()
            if percent:
                on_log(f"Descargando {song.display_name}: {percent}")

    opts = _build_ydl_opts(output_stem, file_format, quality, progress_hook=hook)
    query = f"ytsearch1:{song.search_query}"

    with yt_dlp.YoutubeDL(opts) as ydl:
        if on_log:
            on_log(f"Buscando: {song.search_query}")
        ydl.download([query])

    if expected.exists():
        return expected

    matches = sorted(
        output_dir.glob(f"{base_name}.*"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if matches:
        return matches[0]

    raise RuntimeError(
        f"Descarga completada pero no se encontró el archivo de: {song.display_name}"
    )


class DownloadQueue:
    """Runs downloads on a background thread."""

    def __init__(self) -> None:
        self._thread: threading.Thread | None = None
        self._cancel = threading.Event()

    @property
    def is_running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    def cancel(self) -> None:
        self._cancel.set()

    def start(
        self,
        songs: list[SongQuery],
        output_dir: Path,
        file_format: str,
        quality: str,
        on_log: ProgressCallback | None = None,
        on_item_done: ItemDoneCallback | None = None,
        on_finished: Callable[[], None] | None = None,
    ) -> None:
        if self.is_running:
            raise RuntimeError("Ya hay una descarga en curso.")

        self._cancel.clear()

        def worker() -> None:
            total = len(songs)
            for index, song in enumerate(songs, start=1):
                if self._cancel.is_set():
                    if on_log:
                        on_log("Descarga cancelada.")
                    break
                try:
                    if on_log:
                        on_log(f"[{index}/{total}] {song.display_name}")
                    path = download_song(
                        song,
                        output_dir,
                        file_format,
                        quality,
                        on_log=on_log,
                    )
                    if on_item_done:
                        on_item_done(index, total, song.display_name, True, str(path))
                    if on_log:
                        on_log(f"OK: {path.name}")
                except Exception as exc:  # noqa: BLE001 - report per-item failures
                    if on_item_done:
                        on_item_done(index, total, song.display_name, False, str(exc))
                    if on_log:
                        on_log(f"Error en {song.display_name}: {exc}")
            if on_finished:
                on_finished()

        self._thread = threading.Thread(target=worker, daemon=True)
        self._thread.start()
