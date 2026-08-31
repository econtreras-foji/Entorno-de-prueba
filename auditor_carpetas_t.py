#!/usr/bin/env python3
"""Revisa las carpetas T y genera un reporte de su contenido."""

from __future__ import annotations

import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox, ttk


REPORT_NAME = "reporte_carpetas_T.txt"


def find_t_folders(base_folder: Path) -> list[Path]:
    folders = [path for path in base_folder.rglob("*") if path.is_dir() and path.name.casefold() == "t"]
    if base_folder.name.casefold() == "t":
        folders.append(base_folder)
    return sorted(folders, key=lambda path: str(path.relative_to(base_folder)).casefold())


def count_files(folder: Path) -> int:
    return sum(1 for path in folder.rglob("*") if path.is_file())


def audit_t_folders(base_folder: Path) -> tuple[list[tuple[Path, int]], list[Path]]:
    with_files: list[tuple[Path, int]] = []
    empty: list[Path] = []
    for folder in find_t_folders(base_folder):
        file_count = count_files(folder)
        if file_count:
            with_files.append((folder, file_count))
        else:
            empty.append(folder)
    return with_files, empty


def write_report(base_folder: Path, with_files: list[tuple[Path, int]], empty: list[Path]) -> Path:
    total_folders = len(with_files) + len(empty)
    total_files = sum(file_count for _, file_count in with_files)
    lines = [
        "REPORTE DE CARPETAS T",
        f"Ruta revisada: {base_folder}",
        f"Fecha: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
        "",
        f"Carpetas T revisadas: {total_folders}",
        f"Carpetas T con archivos: {len(with_files)}",
        f"Carpetas T vacías: {len(empty)}",
        f"Total de archivos encontrados en T: {total_files}",
        "",
        "CARPETAS T CON ARCHIVOS",
    ]
    lines.extend(
        f"{folder.relative_to(base_folder)} | {file_count} archivo(s)"
        for folder, file_count in with_files
    )
    if not with_files:
        lines.append("Ninguna.")
    lines.extend(["", "CARPETAS T VACÍAS"])
    lines.extend(str(folder.relative_to(base_folder)) for folder in empty)
    if not empty:
        lines.append("Ninguna.")

    report = base_folder / REPORT_NAME
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report


class AuditorCarpetasTApp(ttk.Frame):
    def __init__(self, window: tk.Tk) -> None:
        super().__init__(window, padding=18)
        self.window = window
        self.base_path = tk.StringVar()
        self.status = tk.StringVar(value="Selecciona la carpeta raíz que contiene los folios.")
        self._build()

    def _build(self) -> None:
        self.window.title("Auditor de Carpetas T")
        self.window.resizable(False, False)
        self.grid(sticky="nsew")
        self.columnconfigure(1, weight=1)

        ttk.Label(self, text="Carpeta raíz:").grid(row=0, column=0, sticky="w", pady=4)
        ttk.Entry(self, textvariable=self.base_path, width=58).grid(row=0, column=1, sticky="ew", padx=8)
        ttk.Button(self, text="Seleccionar", command=self.select_folder).grid(row=0, column=2)
        ttk.Label(self, text="Revisa todas las carpetas llamadas T dentro de la ruta seleccionada.").grid(
            row=1, column=0, columnspan=3, sticky="w", pady=(8, 2)
        )
        ttk.Label(self, text="Genera un bloc de notas con carpetas con archivos y carpetas vacías.").grid(
            row=2, column=0, columnspan=3, sticky="w", pady=2
        )
        ttk.Button(self, text="Revisar carpetas T", command=self.run_audit).grid(row=3, column=2, sticky="e", pady=8)
        ttk.Label(self, textvariable=self.status, wraplength=620).grid(
            row=4, column=0, columnspan=3, sticky="w", pady=(8, 0)
        )

    def select_folder(self) -> None:
        path = filedialog.askdirectory()
        if path:
            self.base_path.set(path)

    def run_audit(self) -> None:
        base_folder = Path(self.base_path.get()).expanduser()
        if not base_folder.is_dir():
            messagebox.showerror("Falta la carpeta", "Selecciona una carpeta raíz válida.")
            return
        try:
            with_files, empty = audit_t_folders(base_folder)
            report = write_report(base_folder, with_files, empty)
        except OSError as error:
            messagebox.showerror("No se pudo revisar", str(error))
            return
        total = len(with_files) + len(empty)
        summary = f"Carpetas T revisadas: {total}. Con archivos: {len(with_files)}. Vacías: {len(empty)}."
        self.status.set(f"{summary} Reporte: {report.name}")
        messagebox.showinfo("Revisión terminada", summary)


def main() -> None:
    window = tk.Tk()
    AuditorCarpetasTApp(window)
    window.mainloop()


if __name__ == "__main__":
    main()
