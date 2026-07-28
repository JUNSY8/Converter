"""First-run terms and conditions acceptance."""

from __future__ import annotations

import os
from pathlib import Path

import customtkinter as ctk

TERMS_TEXT = """TÉRMINOS Y CONDICIONES DE USO

Al usar Descargador de Canciones usted acepta lo siguiente:

1. Uso responsable
   Esta aplicación es una herramienta técnica. Usted es el único
   responsable de cómo la utiliza y del contenido que descarga.

2. Derechos de autor
   Solo puede descargar material si tiene derecho legal a hacerlo
   (por ejemplo, contenido propio, con licencia o en dominio público).
   Queda prohibido usarla para vulnerar derechos de autor u otras leyes.

3. Servicios de terceros
   La búsqueda y descarga pueden depender de servicios externos
   (p. ej. YouTube) y de yt-dlp. Usted debe cumplir también los
   términos de esos servicios.

4. Sin garantías
   El software se ofrece “tal cual”, sin garantías de disponibilidad,
   exactitud o idoneidad. Los autores no responden por daños,
   pérdidas o usos indebidos derivados de la aplicación.

5. Aceptación
   Si no está de acuerdo con estos términos, no use el programa
   y cierre esta ventana sin aceptar.
"""


def terms_accepted_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", str(Path.home() / "AppData" / "Local")))
    return base / "DescargadorCanciones" / "terms_accepted.txt"


def has_accepted_terms() -> bool:
    path = terms_accepted_path()
    return path.is_file() and path.read_text(encoding="utf-8").strip() == "accepted"


def mark_terms_accepted() -> None:
    path = terms_accepted_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("accepted", encoding="utf-8")


class TermsDialog(ctk.CTkToplevel):
    """Modal dialog that requires accepting terms before continuing."""

    def __init__(self, master: ctk.CTk) -> None:
        super().__init__(master)
        self.title("Términos y condiciones")
        self.geometry("560x480")
        self.minsize(480, 400)
        self.resizable(True, True)
        self.accepted = False

        self.transient(master)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self._decline)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            self,
            text="Antes de continuar, lea y acepte los términos",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w",
        ).grid(row=0, column=0, padx=16, pady=(16, 8), sticky="ew")

        box = ctk.CTkTextbox(self, wrap="word")
        box.grid(row=1, column=0, padx=16, pady=8, sticky="nsew")
        box.insert("1.0", TERMS_TEXT)
        box.configure(state="disabled")

        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.grid(row=2, column=0, padx=16, pady=(8, 16), sticky="ew")
        actions.grid_columnconfigure(0, weight=1)

        ctk.CTkButton(
            actions,
            text="No acepto",
            width=120,
            fg_color="gray40",
            hover_color="gray30",
            command=self._decline,
        ).grid(row=0, column=1, padx=(0, 8))

        ctk.CTkButton(
            actions,
            text="Acepto",
            width=140,
            command=self._accept,
        ).grid(row=0, column=2)

        self.after(50, self._center_on_master)

    def _center_on_master(self) -> None:
        self.update_idletasks()
        try:
            mx = self.master.winfo_rootx()
            my = self.master.winfo_rooty()
            mw = self.master.winfo_width()
            mh = self.master.winfo_height()
            w = self.winfo_width()
            h = self.winfo_height()
            self.geometry(f"+{mx + (mw - w) // 2}+{my + (mh - h) // 2}")
        except Exception:  # noqa: BLE001
            pass

    def _accept(self) -> None:
        mark_terms_accepted()
        self.accepted = True
        self.grab_release()
        self.destroy()

    def _decline(self) -> None:
        self.accepted = False
        self.grab_release()
        self.destroy()


def prompt_terms_if_needed(app: ctk.CTk) -> bool:
    """Show terms once; return False if the user declines."""
    if has_accepted_terms():
        return True
    app.update_idletasks()
    dialog = TermsDialog(app)
    app.wait_window(dialog)
    return dialog.accepted
