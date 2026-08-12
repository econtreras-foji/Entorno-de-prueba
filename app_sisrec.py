#!/usr/bin/env python3
"""Interfaz gráfica portable para el organizador SISREC."""

from __future__ import annotations

import contextlib
import io
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from organizador_sisrec import (
    get_coeg_targets,
    get_folios,
    get_id_targets,
    make_structure,
    sort_coeg_files,
    sort_id_files,
)


class OrganizerApp(ttk.Frame):
    def __init__(self, window: tk.Tk) -> None:
        super().__init__(window, padding=18)
        self.window = window
        self.excel_path = tk.StringVar()
        self.destination_path = tk.StringVar(value=str(Path.home() / "Desktop" / "SISREC_JUL_2026"))
        self.source_path = tk.StringVar()
        self.action = tk.StringVar(value="copiar")
        self.recursive = tk.BooleanVar(value=False)
        self.t_source_path = tk.StringVar()
        self.t_action = tk.StringVar(value="copiar")
        self.t_recursive = tk.BooleanVar(value=False)
        self._build()

    def _build(self) -> None:
        self.window.title("Organizador SISREC v6")
        self.window.resizable(False, False)
        self.grid(sticky="nsew")
        self.columnconfigure(1, weight=1)

        ttk.Label(self, text="Excel con los folios:").grid(row=0, column=0, sticky="w", pady=4)
        ttk.Entry(self, textvariable=self.excel_path, width=52).grid(row=0, column=1, sticky="ew", padx=8)
        ttk.Button(self, text="Seleccionar", command=self.select_excel).grid(row=0, column=2)

        ttk.Label(self, text="Carpeta destino:").grid(row=1, column=0, sticky="w", pady=4)
        ttk.Entry(self, textvariable=self.destination_path, width=52).grid(row=1, column=1, sticky="ew", padx=8)
        ttk.Button(self, text="Seleccionar", command=self.select_destination).grid(row=1, column=2)

        ttk.Separator(self).grid(row=2, column=0, columnspan=3, sticky="ew", pady=12)
        ttk.Label(self, text="1. Crear carpetas", font=("Arial", 13, "bold")).grid(row=3, column=0, columnspan=2, sticky="w")
        ttk.Button(self, text="Crear FOLIO / CE / T", command=self.create_structure).grid(row=3, column=2, sticky="e")

        ttk.Separator(self).grid(row=4, column=0, columnspan=3, sticky="ew", pady=12)
        ttk.Label(self, text="2. Ordenar archivos COEG en CE", font=("Arial", 13, "bold")).grid(row=5, column=0, columnspan=3, sticky="w")
        ttk.Label(self, text="Carpeta de archivos:").grid(row=6, column=0, sticky="w", pady=4)
        ttk.Entry(self, textvariable=self.source_path, width=52).grid(row=6, column=1, sticky="ew", padx=8)
        ttk.Button(self, text="Seleccionar", command=self.select_source).grid(row=6, column=2)

        options = ttk.Frame(self)
        options.grid(row=7, column=0, columnspan=3, sticky="w", pady=6)
        ttk.Label(
            options,
            text="COEG va a CE; NOMINA-<COEG_NUMERO> se copia en todos los T coincidentes.",
        ).grid(row=0, column=0, padx=(0, 16))
        ttk.Label(options, text="Acción:").grid(row=0, column=1, padx=(0, 4))
        ttk.Combobox(options, textvariable=self.action, values=("copiar", "mover"), state="readonly", width=8).grid(row=0, column=2, padx=(0, 16))
        ttk.Checkbutton(options, text="Buscar en subcarpetas", variable=self.recursive).grid(row=0, column=3)
        ttk.Button(self, text="Ordenar archivos", command=self.sort).grid(row=8, column=2, sticky="e", pady=8)

        ttk.Separator(self).grid(row=9, column=0, columnspan=3, sticky="ew", pady=12)
        ttk.Label(self, text="3. Ordenar respaldos ID en T", font=("Arial", 13, "bold")).grid(row=10, column=0, columnspan=3, sticky="w")
        ttk.Label(self, text="Carpeta de respaldos:").grid(row=11, column=0, sticky="w", pady=4)
        ttk.Entry(self, textvariable=self.t_source_path, width=52).grid(row=11, column=1, sticky="ew", padx=8)
        ttk.Button(self, text="Seleccionar", command=self.select_t_source).grid(row=11, column=2)
        t_options = ttk.Frame(self)
        t_options.grid(row=12, column=0, columnspan=3, sticky="w", pady=6)
        ttk.Label(t_options, text="Se excluyen los documentos “Convenio Becados”.").grid(row=0, column=0, padx=(0, 16))
        ttk.Label(t_options, text="Acción:").grid(row=0, column=1, padx=(0, 4))
        ttk.Combobox(t_options, textvariable=self.t_action, values=("copiar", "mover"), state="readonly", width=8).grid(row=0, column=2, padx=(0, 16))
        ttk.Checkbutton(t_options, text="Buscar en subcarpetas", variable=self.t_recursive).grid(row=0, column=3)
        ttk.Button(self, text="Ordenar respaldos en T", command=self.sort_t).grid(row=13, column=2, sticky="e", pady=8)
        self.status = tk.StringVar(value="Selecciona el Excel para comenzar.")
        ttk.Label(self, textvariable=self.status, wraplength=580).grid(row=14, column=0, columnspan=3, sticky="w", pady=(8, 0))

    def select_excel(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("Archivos Excel", "*.xlsx *.xlsm")])
        if path:
            self.excel_path.set(path)

    def select_destination(self) -> None:
        path = filedialog.askdirectory()
        if path:
            self.destination_path.set(path)

    def select_source(self) -> None:
        path = filedialog.askdirectory()
        if path:
            self.source_path.set(path)

    def select_t_source(self) -> None:
        path = filedialog.askdirectory()
        if path:
            self.t_source_path.set(path)

    def folios(self) -> list[str] | None:
        excel = Path(self.excel_path.get()).expanduser()
        if not excel.is_file():
            messagebox.showerror("Falta el Excel", "Selecciona un archivo Excel válido.")
            return None
        try:
            return get_folios(excel, "base SISREC")
        except (OSError, ValueError) as error:
            messagebox.showerror("No se pudo leer el Excel", str(error))
            return None

    def create_structure(self) -> None:
        folios = self.folios()
        if not folios:
            return
        destination = Path(self.destination_path.get()).expanduser()
        if not messagebox.askyesno("Confirmar", f"Se crearán {len(folios)} carpetas en:\n{destination}"):
            return
        make_structure(destination, folios, True)
        self.status.set(f"Estructura creada: {len(folios)} carpetas con CE y T.")
        messagebox.showinfo("Completado", "Las carpetas fueron creadas correctamente.")

    def sort(self) -> None:
        folios = self.folios()
        source = Path(self.source_path.get()).expanduser()
        if not folios or not source.is_dir():
            if folios:
                messagebox.showerror("Falta la carpeta", "Selecciona la carpeta que contiene los archivos.")
            return
        action_text = "moverán" if self.action.get() == "mover" else "copiarán"
        confirmation = (
            f"Los archivos COEG se {action_text} en CE.\n\n"
            "Los archivos llamados NOMINA-<COEG_NUMERO> se copiarán en todos los T del mismo COEG.\n"
            "El archivo original se mantendrá en la carpeta de origen.\n\n"
            "¿Deseas continuar?"
        )
        if not messagebox.askyesno("Confirmar ordenamiento", confirmation):
            return
        try:
            targets = get_coeg_targets(Path(self.excel_path.get()).expanduser(), "base SISREC")
        except (OSError, ValueError) as error:
            messagebox.showerror("No se pudo leer el Excel", str(error))
            return
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            sort_coeg_files(Path(self.destination_path.get()).expanduser(), source, targets, self.action.get(), self.recursive.get(), True)
        result = output.getvalue().splitlines()
        summary = result[-1] if result else "Proceso terminado."
        self.status.set(summary)
        messagebox.showinfo("Completado", summary)

    def sort_t(self) -> None:
        folios = self.folios()
        source = Path(self.t_source_path.get()).expanduser()
        if not folios or not source.is_dir():
            if folios:
                messagebox.showerror("Falta la carpeta", "Selecciona la carpeta que contiene los respaldos.")
            return
        if self.t_action.get() == "mover" and not messagebox.askyesno("Confirmar movimiento", "Los archivos originales se moverán. ¿Deseas continuar?"):
            return
        try:
            targets = get_id_targets(Path(self.excel_path.get()).expanduser(), "base SISREC")
        except (OSError, ValueError) as error:
            messagebox.showerror("No se pudo leer el Excel", str(error))
            return
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            sort_id_files(Path(self.destination_path.get()).expanduser(), source, targets, self.t_action.get(), self.t_recursive.get(), True)
        result = output.getvalue().splitlines()
        summary = result[-1] if result else "Proceso terminado."
        self.status.set(summary)
        messagebox.showinfo("Completado", summary)


def main() -> None:
    window = tk.Tk()
    OrganizerApp(window)
    window.mainloop()


if __name__ == "__main__":
    main()
