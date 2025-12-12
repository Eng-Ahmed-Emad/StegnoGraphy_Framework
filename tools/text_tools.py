"""
Text Steganography Tools
S-Tools and SNOW
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import os
from .base_tool import BaseToolWindow, find_executable, launch_executable


class TextStegoWindow:
    """Window for Text Steganography tools"""
    
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Text Steganography Tools")
        self.window.geometry("750x650")
        
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # WBStego tab (launcher)
        wb_frame = ttk.Frame(notebook)
        notebook.add(wb_frame, text="WBStego4Open")
        self.wb_tool = WBStegoTool(wb_frame, self.window)

        # Auto-launch when its tab is selected
        def _on_text_tab_changed(event):
            try:
                selected = notebook.tab(notebook.select(), "text")
                if selected == "WBStego4Open":
                    self.wb_tool.launch_wbsteo()
            except Exception:
                pass

        notebook.bind('<<NotebookTabChanged>>', _on_text_tab_changed)
        
        # Handle window close event
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_closing(self):
        """Handle window closing event"""
        try:
            # Close the window
            self.window.destroy()
        except Exception:
            pass


class WBStegoTool:
    """WBStego4Open launcher tool"""

    def __init__(self, parent, root_window):
        self.parent = parent
        self.root_window = root_window
        lbl = ttk.Label(parent, text="WBStego4Open Launcher", font=(None, 11, "bold"))
        lbl.pack(anchor="w", padx=10, pady=(8, 4))

        info = ttk.Label(parent, text="Launch the WBStego4Open GUI application to hide or extract messages in text files.")
        info.pack(anchor="w", padx=10, pady=(0, 8))

        btn_log = ttk.Button(parent, text="Launch with logs", command=self.launch_wbsteo_with_logging)
        btn_log.pack(anchor="w", padx=10, pady=(0, 8))

    def launch_wbsteo(self):
        wb_path = self.find_wbsteo()

        def try_open(path):
            tools_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            wbs_dir = os.path.join(tools_dir, 'wbs43open-win32')
            cwd = wbs_dir if os.path.isdir(wbs_dir) else None
            ok = launch_executable(path, cwd=cwd)
            if ok:
                messagebox.showinfo("Success", "WBStego4Open GUI application opened!\nUse the application to hide or extract messages.")
            else:
                messagebox.showerror("Error", f"Failed to open WBStego4Open: \n{path}")
            return ok
    def find_wbsteo(self):
        """Find WBStego4Open executable or shortcut"""
        possible_paths = [
            os.path.join(os.path.dirname(__file__), "wbStego4.3open.exe"),
            os.path.join(os.path.dirname(__file__), "wbStego4.3open.exe.lnk"),
            os.path.join(os.path.dirname(__file__), "wbs43open-win32", "wbStego4.3open.exe"),
            os.path.join(os.path.dirname(__file__), "..", "Tools", "wbStego4.3open.exe"),
            os.path.join(os.path.dirname(__file__), "..", "tools", "wbStego4.3open.exe"),
            os.path.join(os.path.dirname(__file__), "..", "Tools", "wbs43open-win32", "wbStego4.3open.exe"),
            os.path.join(os.path.dirname(__file__), "..", "Tools", "WBStego4Open.exe"),
            "wbStego4.3open.exe",
            "WBStego4Open.exe",
            "WBStego4.3open.exe",
        ]
        return find_executable(possible_paths)

    def launch_wbsteo_with_logging(self):
        """Launch WBStego but capture stdout/stderr to a log file for debugging"""
        wb_path = self.find_wbsteo()
        if not wb_path:
            messagebox.showerror("Error", "WBStego executable not found. Please ensure wbStego4.3open.exe is in the tools folder.")
            return

        abs_path = os.path.abspath(wb_path)
        tools_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        wbs_dir = os.path.join(tools_dir, 'wbs43open-win32')
        cwd = wbs_dir if os.path.isdir(wbs_dir) else os.path.dirname(abs_path)

        log_path = os.path.join(tools_dir, 'wbsteo_launch_log.txt')
        try:
            result = subprocess.run([abs_path], cwd=cwd, capture_output=True, timeout=30)
            with open(log_path, 'wb') as f:
                f.write(result.stdout or b'')
                f.write(b"\n--- STDERR ---\n")
                f.write(result.stderr or b'')
            messagebox.showinfo("Launched", f"WBStego launched and logs written to:\n{log_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch WBStego: {e}\nLogs: {log_path}")
    # SNOW support removed - SNOW detection/commands are no longer part of this toolkit
    
    
    # SNOW support removed - SNOW detection/commands are no longer part of this toolkit


    # S-Tools support removed - S-Tools detection/commands are no longer part of this toolkit

