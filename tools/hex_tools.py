"""
Hex/Binary Steganography Tools
HxD
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
from .base_tool import BaseToolWindow, find_executable, launch_executable


class HexStegoWindow:
    """Window for Hex/Binary Steganography tools"""
    
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Hex/Binary Steganography Tools")
        self.window.geometry("750x650")
        
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # HxD tab
        hxd_frame = ttk.Frame(notebook)
        notebook.add(hxd_frame, text="HxD")
        self.hxd_tool = HxDTool(hxd_frame, self.window)
        
        # GMER removed from GUI - HxD is the primary tool

        # Auto-open HxD when its tab is selected
        def _on_hex_tab_changed(event):
            try:
                selected = notebook.tab(notebook.select(), "text")
                if selected == "HxD":
                    self.hxd_tool.open_hxd()
            except Exception:
                pass

        notebook.bind('<<NotebookTabChanged>>', _on_hex_tab_changed)


    # Hex Editor Neo removed from toolkit - HxD is used instead


class HxDTool(BaseToolWindow):
    """HxD hex editor launcher"""

    def __init__(self, parent, root_window):
        self.root_window = root_window
        super().__init__(parent, "HxD")

    def open_hxd(self):
        """Open HxD executable, optionally with input file"""
        self.clear_log("hide")
        self.log("Opening HxD...", tab="hide")

        hxd_path = self.find_hxd()
        def try_open(path):
            args = []
            if self.input_file.get() and os.path.exists(self.input_file.get()):
                args = [self.input_file.get()]
            ok = launch_executable(path, extra_args=args)
            if ok:
                self.log(f"HxD opened successfully: {path}", "SUCCESS", tab="hide")
                messagebox.showinfo("Success", "HxD opened! Use it to inspect or modify binary files.")
                return True
            else:
                self.log(f"Error opening HxD: {path}", "ERROR", tab="hide")
                messagebox.showerror("Error", f"Failed to open HxD:\n{path}")
                return False

        if hxd_path and try_open(hxd_path):
            return

        # Ask user to locate HxD
        from tkinter import filedialog
        user_choice = filedialog.askopenfilename(
            title="Locate HxD executable",
            initialdir=os.path.abspath(os.path.join(os.path.dirname(__file__), '..')),
            filetypes=[("Executables", "*.exe;*.lnk"), ("All files", "*.*")]
        )
        if user_choice:
            try_open(user_choice)

    def find_hxd(self):
        possible_paths = [
            os.path.join(os.path.dirname(__file__), "HxD.exe"),
            os.path.join(os.path.dirname(__file__), "HxD.exe.lnk"),
            os.path.join(os.path.dirname(__file__), "..", "Tools", "HxD.exe"),
            os.path.join(os.path.dirname(__file__), "..", "tools", "HxD.exe"),
            "HxD.exe",
            "HxD64.exe",
            "hxd.exe",
        ]
        return find_executable(possible_paths)



    # GMER removed from toolkit

