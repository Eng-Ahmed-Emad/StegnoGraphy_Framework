"""
ADS (Alternate Data Streams) Tools
ADS Viewer only
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os


class ADSToolsWindow:
    """Window for ADS Tools"""
    
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("ADS Tools")
        self.window.geometry("750x650")
        
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ADS Viewer tab
        adsviewer_frame = ttk.Frame(notebook)
        notebook.add(adsviewer_frame, text="ADS Viewer")
        self.adsviewer_tool = ADSViewerTool(adsviewer_frame, self.window)


class ADSViewerTool:
    """ADS Viewer tool - simple GUI launcher"""
    
    def __init__(self, parent, root_window):
        self.root_window = root_window
        self.parent = parent
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the UI"""
        # Simple frame with button to launch ADS Viewer
        frame = ttk.Frame(self.parent, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="ADS Viewer", font=("Arial", 14, "bold")).pack(pady=10)
        ttk.Label(frame, text="This tool provides a GUI to view and manage\nAlternate Data Streams.", 
                 font=("Arial", 10), justify=tk.CENTER).pack(pady=10)
        
        ttk.Button(frame, text="Open ADS Viewer", command=self.launch_viewer, width=30).pack(pady=20)
        
        ttk.Label(frame, text="ADS Viewer allows you to:\n• View all streams in a file\n• Create/Delete streams\n• View stream contents",
                 font=("Arial", 9), justify=tk.LEFT).pack(pady=10, anchor=tk.W)
    
    def find_ads_viewer(self):
        """Find ADS Viewer executable"""
        possible_paths = [
            "D:\\ADSView.exe",
            os.path.join(os.path.dirname(__file__), "..", "Tools", "ADSViewer.exe"),
            os.path.join(os.path.dirname(__file__), "..", "tools", "ADSViewer.exe"),
            os.path.join(os.path.dirname(__file__), "..", "Tools", "ADS Viewer.exe"),
            "ADSViewer.exe",
            "adsviewer.exe",
        ]
        for path in possible_paths:
            abs_path = os.path.abspath(path)
            if os.path.exists(abs_path):
                return abs_path
        return None
    
    def launch_viewer(self):
        """Launch ADS Viewer GUI"""
        adsviewer_path = self.find_ads_viewer()
        if adsviewer_path:
            try:
                subprocess.Popen([adsviewer_path])
                messagebox.showinfo("Success", "ADS Viewer launched successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to launch ADS Viewer:\n{str(e)}")
        else:
            messagebox.showerror("Error", "ADSView.exe not found.\nPlease ensure it's in D:\\ or the Tools folder.")
