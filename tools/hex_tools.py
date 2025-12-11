"""
Hex/Binary Steganography Tools
Hex Editor Neo and GMER
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
from .base_tool import BaseToolWindow


class HexStegoWindow:
    """Window for Hex/Binary Steganography tools"""
    
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Hex/Binary Steganography Tools")
        self.window.geometry("750x650")
        
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Hex Editor Neo tab
        hexneo_frame = ttk.Frame(notebook)
        notebook.add(hexneo_frame, text="Hex Editor Neo")
        self.hexneo_tool = HexEditorNeoTool(hexneo_frame, self.window)
        
        # GMER tab
        gmer_frame = ttk.Frame(notebook)
        notebook.add(gmer_frame, text="GMER")
        self.gmer_tool = GMERTool(gmer_frame, self.window)


class HexEditorNeoTool(BaseToolWindow):
    """Hex Editor Neo tool implementation"""
    
    def __init__(self, parent, root_window):
        self.root_window = root_window
        super().__init__(parent, "Hex Editor Neo")
    
    def create_hide_tab(self, parent):
        """Create Hide tab with binary file types"""
        super().create_hide_tab(parent)
        # Update browse buttons for binary files
        for widget in parent.winfo_children():
            if isinstance(widget, ttk.Button) and widget.cget("text") == "Browse":
                info = widget.grid_info()
                if info.get("row") == 0:
                    widget.config(command=lambda: self.browse_input_file([
                        ("Binary files", "*.bin *.exe *.dll *.dat"), ("All files", "*.*")
                    ]))
                elif info.get("row") == 1:
                    widget.config(command=lambda: self.browse_output_file([
                        ("Binary files", "*.bin *.exe *.dll *.dat"), ("All files", "*.*")
                    ]))
    
    def create_extract_tab(self, parent):
        """Create Extract tab with binary file types"""
        super().create_extract_tab(parent)
        # Update browse button for binary files
        for widget in parent.winfo_children():
            if isinstance(widget, ttk.Button) and widget.cget("text") == "Browse":
                widget.config(command=lambda: self.browse_input_file([
                    ("Binary files", "*.bin *.exe *.dll *.dat"), ("All files", "*.*")
                ]))
    
    def hide_message(self):
        """Hide message - Launch Hex Editor Neo"""
        self.clear_log("hide")
        self.log("Opening Hex Editor Neo...", tab="hide")
        
        hexneo_path = self.find_hexneo()
        if hexneo_path:
            try:
                # Open with input file if provided
                if self.input_file.get() and os.path.exists(self.input_file.get()):
                    subprocess.Popen([hexneo_path, self.input_file.get()])
                else:
                    subprocess.Popen([hexneo_path])
                self.log(f"Hex Editor Neo opened successfully: {hexneo_path}", "SUCCESS", tab="hide")
                messagebox.showinfo("Success", "Hex Editor Neo opened!\nUse the hex editor to manually hide your message in the binary file.")
            except Exception as e:
                self.log(f"Error opening Hex Editor Neo: {str(e)}", "ERROR", tab="hide")
                messagebox.showerror("Error", f"Failed to open Hex Editor Neo:\n{str(e)}")
        else:
            self.log("Hex Editor Neo not found.", "ERROR", tab="hide")
            messagebox.showwarning("Not Found", "Hex Editor Neo executable not found.\nPlease install Hex Editor Neo for full functionality.")
    
    def extract_message(self):
        """Extract message - Launch Hex Editor Neo"""
        self.clear_log("extract")
        self.log("Opening Hex Editor Neo...", tab="extract")
        
        hexneo_path = self.find_hexneo()
        if hexneo_path:
            try:
                # Open with input file if provided
                if self.input_file.get() and os.path.exists(self.input_file.get()):
                    subprocess.Popen([hexneo_path, self.input_file.get()])
                else:
                    subprocess.Popen([hexneo_path])
                self.log(f"Hex Editor Neo opened successfully: {hexneo_path}", "SUCCESS", tab="extract")
                messagebox.showinfo("Success", "Hex Editor Neo opened!\nUse the hex editor to manually extract the hidden message from the binary file.")
            except Exception as e:
                self.log(f"Error opening Hex Editor Neo: {str(e)}", "ERROR", tab="extract")
                messagebox.showerror("Error", f"Failed to open Hex Editor Neo:\n{str(e)}")
        else:
            self.log("Hex Editor Neo not found.", "ERROR", tab="extract")
            messagebox.showwarning("Not Found", "Hex Editor Neo executable not found.\nPlease install Hex Editor Neo for full functionality.")
    
    def find_hexneo(self):
        """Find Hex Editor Neo executable"""
        possible_paths = [
            "HxD.exe",
            "hexeditor.exe",
            "HexEditorNeo.exe",
            os.path.join(os.path.dirname(__file__), "..", "Tools", "HexEditorNeo.exe"),
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
        return None


class GMERTool(BaseToolWindow):
    """GMER tool implementation"""
    
    def __init__(self, parent, root_window):
        self.root_window = root_window
        super().__init__(parent, "GMER")
    
    def create_hide_tab(self, parent):
        """Create Hide tab - GMER doesn't hide, just opens GUI"""
        super().create_hide_tab(parent)
        # Update browse buttons for executable files
        for widget in parent.winfo_children():
            if isinstance(widget, ttk.Button) and widget.cget("text") == "Browse":
                info = widget.grid_info()
                if info.get("row") == 0:
                    widget.config(command=lambda: self.browse_input_file([
                        ("Executable files", "*.exe *.dll *.sys"), ("All files", "*.*")
                    ]))
                elif info.get("row") == 1:
                    widget.config(command=lambda: self.browse_output_file([
                        ("Text files", "*.txt"), ("All files", "*.*")
                    ]))
    
    def create_extract_tab(self, parent):
        """Create Extract tab with executable file types"""
        super().create_extract_tab(parent)
        # Update browse button for executable files
        for widget in parent.winfo_children():
            if isinstance(widget, ttk.Button) and widget.cget("text") == "Browse":
                widget.config(command=lambda: self.browse_input_file([
                    ("Executable files", "*.exe *.dll *.sys"), ("All files", "*.*")
                ]))
    
    def hide_message(self):
        """Hide message - Launch GMER (GMER doesn't hide, but opens for analysis)"""
        self.clear_log("hide")
        self.log("Opening GMER...", tab="hide")
        
        gmer_path = self.find_gmer()
        if gmer_path:
            try:
                subprocess.Popen([gmer_path], shell=True)
                self.log(f"GMER opened successfully: {gmer_path}", "SUCCESS", tab="hide")
                messagebox.showinfo("Success", "GMER opened!\nGMER is a security analysis tool. Use it to analyze binary files.")
            except Exception as e:
                self.log(f"Error opening GMER: {str(e)}", "ERROR", tab="hide")
                messagebox.showerror("Error", f"Failed to open GMER:\n{str(e)}")
        else:
            self.log("GMER not found.", "ERROR", tab="hide")
            messagebox.showwarning("Not Found", "GMER executable not found.\nPlease install GMER for full functionality.")
    
    def open_gmer(self):
        """Open GMER tool"""
        self.hide_message()  # Reuse hide_message to open GMER
    
    def analyze_binary(self):
        """Analyze binary file"""
        if not self.validate_inputs(require_message=False, require_password=False, tab="hide"):
            return
        
        self.clear_log("hide")
        self.log("Analyzing binary file...", tab="hide")
        
        try:
            file_path = self.input_file.get()
            file_size = os.path.getsize(file_path)
            
            self.log(f"File: {file_path}", "INFO", tab="hide")
            self.log(f"Size: {file_size} bytes", "INFO", tab="hide")
            self.log("Analysis complete.", "SUCCESS", tab="hide")
            self.log("Note: Use GMER for detailed rootkit and hidden data analysis.", "INFO", tab="hide")
        
        except Exception as e:
            self.log(f"Exception: {str(e)}", "ERROR", tab="hide")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def extract_message(self):
        """Extract hidden data - Launch GMER"""
        self.clear_log("extract")
        self.log("Opening GMER...", tab="extract")
        
        gmer_path = self.find_gmer()
        if gmer_path:
            try:
                subprocess.Popen([gmer_path], shell=True)
                self.log(f"GMER opened successfully: {gmer_path}", "SUCCESS", tab="extract")
                messagebox.showinfo("Success", "GMER opened!\nUse GMER for detailed binary analysis and hidden data extraction.")
            except Exception as e:
                self.log(f"Error opening GMER: {str(e)}", "ERROR", tab="extract")
                messagebox.showerror("Error", f"Failed to open GMER:\n{str(e)}")
        else:
            self.log("GMER not found.", "ERROR", tab="extract")
            messagebox.showwarning("Not Found", "GMER executable not found.\nPlease install GMER for full functionality.")
    
    def find_gmer(self):
        """Find GMER executable"""
        possible_paths = [
            "gmer.exe",
            "GMER.exe",
            os.path.join(os.path.dirname(__file__), "..", "Tools", "gmer.exe"),
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
        return None

