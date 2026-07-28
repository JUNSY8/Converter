"""Desktop UI for downloading songs by title and artist."""

from __future__ import annotations

import random
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk

from downloader import (
    AUDIO_QUALITIES,
    VIDEO_QUALITIES,
    DownloadQueue,
    ffmpeg_available,
    parse_song_list,
)

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class SongDownloaderApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Descargador de canciones")
        self.geometry("780x640")
        self.minsize(680, 560)

        self.queue = DownloadQueue()
        self.output_dir = ctk.StringVar(value=str(Path.home() / "Downloads" / "Canciones"))
        self.file_format = ctk.StringVar(value="MP3")
        self.quality = ctk.StringVar(value="192")
        self.random_mode = ctk.BooleanVar(value=False)
        self.status_text = ctk.StringVar(value="Listo.")
        self._completed = 0
        self._failed = 0

        self._build_ui()
        self._update_quality_options()
        self._check_ffmpeg()

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_ui(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(4, weight=1)

        header = ctk.CTkLabel(
            self,
            text="Descargador de canciones",
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        header.grid(row=0, column=0, padx=20, pady=(18, 8), sticky="w")

        list_frame = ctk.CTkFrame(self)
        list_frame.grid(row=1, column=0, padx=20, pady=8, sticky="nsew")
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            list_frame,
            text="Lista de canciones (una por línea: Título - Autor)",
            anchor="w",
        ).grid(row=0, column=0, padx=12, pady=(12, 4), sticky="ew")

        self.songs_box = ctk.CTkTextbox(list_frame, wrap="word")
        self.songs_box.grid(row=1, column=0, padx=12, pady=(0, 12), sticky="nsew")
        self.songs_box.insert(
            "1.0",
            "Bohemian Rhapsody - Queen\nBlinding Lights, The Weeknd\n",
        )

        options = ctk.CTkFrame(self)
        options.grid(row=2, column=0, padx=20, pady=8, sticky="ew")
        options.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(options, text="Formato").grid(row=0, column=0, padx=(12, 6), pady=12)
        self.format_menu = ctk.CTkOptionMenu(
            options,
            values=["MP3", "MP4"],
            variable=self.file_format,
            command=self._on_format_change,
            width=100,
        )
        self.format_menu.grid(row=0, column=1, padx=6, pady=12, sticky="w")

        ctk.CTkLabel(options, text="Calidad").grid(row=0, column=2, padx=(18, 6), pady=12)
        self.quality_menu = ctk.CTkOptionMenu(
            options,
            values=list(AUDIO_QUALITIES),
            variable=self.quality,
            width=120,
        )
        self.quality_menu.grid(row=0, column=3, padx=6, pady=12, sticky="w")

        ctk.CTkLabel(options, text="Carpeta").grid(row=1, column=0, padx=(12, 6), pady=(0, 12))
        self.folder_entry = ctk.CTkEntry(options, textvariable=self.output_dir)
        self.folder_entry.grid(row=1, column=1, columnspan=2, padx=6, pady=(0, 12), sticky="ew")
        ctk.CTkButton(options, text="Elegir...", width=90, command=self._choose_folder).grid(
            row=1, column=3, padx=(6, 12), pady=(0, 12)
        )

        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.grid(row=3, column=0, padx=20, pady=4, sticky="ew")
        actions.grid_columnconfigure(3, weight=1)

        self.progress = ctk.CTkProgressBar(actions)
        self.progress.grid(row=0, column=0, columnspan=4, sticky="ew", pady=(0, 8))
        self.progress.set(0)

        self.download_btn = ctk.CTkButton(
            actions, text="Descargar", width=140, command=self._start_download
        )
        self.download_btn.grid(row=1, column=0, sticky="w")

        self.random_btn = ctk.CTkButton(
            actions,
            text="Aleatorio: OFF",
            width=130,
            fg_color="gray40",
            hover_color="gray30",
            command=self._toggle_random_mode,
        )
        self.random_btn.grid(row=1, column=1, padx=8, sticky="w")

        self.cancel_btn = ctk.CTkButton(
            actions,
            text="Cancelar",
            width=120,
            fg_color="gray40",
            hover_color="gray30",
            state="disabled",
            command=self._cancel_download,
        )
        self.cancel_btn.grid(row=1, column=2, padx=8, sticky="w")

        ctk.CTkLabel(actions, textvariable=self.status_text, anchor="w").grid(
            row=1, column=3, sticky="ew", padx=(8, 0)
        )

        log_frame = ctk.CTkFrame(self)
        log_frame.grid(row=4, column=0, padx=20, pady=(8, 18), sticky="nsew")
        log_frame.grid_columnconfigure(0, weight=1)
        log_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(log_frame, text="Registro", anchor="w").grid(
            row=0, column=0, padx=12, pady=(12, 4), sticky="ew"
        )
        self.log_box = ctk.CTkTextbox(log_frame, wrap="word", state="disabled")
        self.log_box.grid(row=1, column=0, padx=12, pady=(0, 12), sticky="nsew")

    def _check_ffmpeg(self) -> None:
        if not ffmpeg_available():
            self._append_log(
                "AVISO: ffmpeg no está en el PATH. Instálalo y reinicia la app "
                "(ver README.md)."
            )
            self.status_text.set("ffmpeg no encontrado")

    def _on_format_change(self, _value: str) -> None:
        self._update_quality_options()

    def _update_quality_options(self) -> None:
        if self.file_format.get().upper() == "MP3":
            values = list(AUDIO_QUALITIES)
            labels = [f"{q} kbps" for q in values]
            self._quality_map = dict(zip(labels, values, strict=True))
            default_label = "192 kbps"
        else:
            values = list(VIDEO_QUALITIES)
            labels = [f"{q}p" for q in values]
            self._quality_map = dict(zip(labels, values, strict=True))
            default_label = "720p"

        self.quality_menu.configure(values=labels)
        self.quality_menu.set(default_label)
        self.quality.set(self._quality_map[default_label])

    def _resolved_quality(self) -> str:
        selected = self.quality_menu.get()
        return self._quality_map.get(selected, selected.split()[0].replace("p", "").replace("kbps", ""))

    def _choose_folder(self) -> None:
        chosen = filedialog.askdirectory(initialdir=self.output_dir.get())
        if chosen:
            self.output_dir.set(chosen)

    def _append_log(self, message: str) -> None:
        self.log_box.configure(state="normal")
        self.log_box.insert("end", message + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def _ui(self, func, *args) -> None:
        self.after(0, lambda: func(*args))

    def _set_busy(self, busy: bool) -> None:
        self.download_btn.configure(state="disabled" if busy else "normal")
        self.cancel_btn.configure(state="normal" if busy else "disabled")
        self.format_menu.configure(state="disabled" if busy else "normal")
        self.quality_menu.configure(state="disabled" if busy else "normal")
        self.random_btn.configure(state="disabled" if busy else "normal")

    def _toggle_random_mode(self) -> None:
        active = not self.random_mode.get()
        self.random_mode.set(active)
        if active:
            self.random_btn.configure(
                text="Aleatorio: ON",
                fg_color=["#2CC985", "#2FA572"],
                hover_color=["#25A36C", "#26865E"],
            )
            self.status_text.set("Modo aleatorio activo")
        else:
            self.random_btn.configure(
                text="Aleatorio: OFF",
                fg_color="gray40",
                hover_color="gray30",
            )
            self.status_text.set("Modo aleatorio desactivado")

    def _start_download(self) -> None:
        if self.queue.is_running:
            return

        if not ffmpeg_available():
            messagebox.showerror(
                "ffmpeg requerido",
                "No se encontró ffmpeg en el PATH.\n"
                "Instálalo (por ejemplo: winget install ffmpeg) y reinicia la app.",
            )
            return

        songs = parse_song_list(self.songs_box.get("1.0", "end"))
        if not songs:
            messagebox.showwarning("Lista vacía", "Agrega al menos una canción.")
            return

        output = Path(self.output_dir.get().strip())
        if not self.output_dir.get().strip():
            messagebox.showwarning("Carpeta", "Elige una carpeta de destino.")
            return

        file_format = self.file_format.get().lower()
        quality = self._resolved_quality()
        shuffle = self.random_mode.get()
        if shuffle:
            songs = list(songs)
            random.shuffle(songs)

        self._completed = 0
        self._failed = 0
        self.progress.set(0)
        self._set_busy(True)
        self.status_text.set(f"Descargando 0/{len(songs)}…")
        order_note = "orden aleatorio" if shuffle else "orden de la lista"
        self._append_log(
            f"--- Inicio: {len(songs)} canción(es), {file_format.upper()} @ {quality}, "
            f"{order_note} → {output}"
        )
        if shuffle:
            self._append_log(
                "Orden de descarga: "
                + " | ".join(song.display_name for song in songs)
            )

        def on_log(msg: str) -> None:
            self._ui(self._append_log, msg)

        def on_item_done(index: int, total: int, name: str, ok: bool, detail: str) -> None:
            def update() -> None:
                if ok:
                    self._completed += 1
                else:
                    self._failed += 1
                self.progress.set(index / total)
                self.status_text.set(f"Descargando {index}/{total}…")

            self._ui(update)

        def on_finished() -> None:
            def update() -> None:
                self._set_busy(False)
                total_ok = self._completed
                total_fail = self._failed
                self.status_text.set(f"Listo. OK: {total_ok} | Errores: {total_fail}")
                self.progress.set(1)
                self._append_log(
                    f"--- Fin. Completadas: {total_ok}, errores: {total_fail}"
                )
                if total_fail and not total_ok:
                    messagebox.showwarning(
                        "Finalizado con errores",
                        "No se pudo descargar ninguna canción. Revisa el registro.",
                    )
                elif total_fail:
                    messagebox.showinfo(
                        "Finalizado",
                        f"Descargas OK: {total_ok}\nErrores: {total_fail}",
                    )

            self._ui(update)

        try:
            self.queue.start(
                songs=songs,
                output_dir=output,
                file_format=file_format,
                quality=quality,
                on_log=on_log,
                on_item_done=on_item_done,
                on_finished=on_finished,
            )
        except RuntimeError as exc:
            self._set_busy(False)
            messagebox.showerror("Error", str(exc))

    def _cancel_download(self) -> None:
        if self.queue.is_running:
            self.queue.cancel()
            self.status_text.set("Cancelando…")
            self._append_log("Cancelación solicitada…")

    def _on_close(self) -> None:
        if self.queue.is_running:
            if not messagebox.askyesno(
                "Salir",
                "Hay una descarga en curso. ¿Cancelar y salir?",
            ):
                return
            self.queue.cancel()
        self.destroy()


def main() -> None:
    app = SongDownloaderApp()
    app.mainloop()


if __name__ == "__main__":
    main()
