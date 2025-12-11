"""
Text Steganography Tools
WBStego4Open and S-Tools
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import os
from .base_tool import BaseToolWindow


class TextStegoWindow:
    """Window for Text Steganography tools"""
    
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Text Steganography Tools")
        self.window.geometry("750x650")
        
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # S-Tools tab (show first)
        stools_frame = ttk.Frame(notebook)
        notebook.add(stools_frame, text="S-Tools")
        self.stools_tool = SToolsTool(stools_frame, self.window)

        # WBStego4Open tab
        wbstego_frame = ttk.Frame(notebook)
        notebook.add(wbstego_frame, text="WBStego4Open")
        self.wbstego_tool = WBStegoTool(wbstego_frame, self.window)

        # Open WBStego GUI immediately when its tab is selected (no input validation)
        def _on_tab_changed(event):
            try:
                selected = notebook.tab(notebook.select(), "text")
                if selected == "WBStego4Open":
                    # attempt to open the WBStego application immediately
                    try:
                        self.wbstego_tool.open_wbstego()
                    except Exception:
                        # Fallback: call hide_message if open_wbstego isn't available
                        try:
                            self.wbstego_tool.hide_message()
                        except Exception:
                            pass
            except Exception:
                pass

        notebook.bind('<<NotebookTabChanged>>', _on_tab_changed)


class WBStegoTool(BaseToolWindow):
    """WBStego4Open tool implementation"""
    
    def __init__(self, parent, root_window):
        self.root_window = root_window
        super().__init__(parent, "WBStego4Open")

    def open_wbstego(self):
        """Open the WBStego GUI application without validating input fields."""
        self.clear_log("hide")
        self.log("Opening WBStego GUI application...", tab="hide")

        wbstego_path = self.find_wbstego()
        if not wbstego_path:
            # Prompt user to locate the executable
            user_choice = filedialog.askopenfilename(
                title="Locate WBStego executable",
                initialdir=os.path.abspath(os.path.join(os.path.dirname(__file__), '..')),
                filetypes=[("Executables", "*.exe"), ("All files", "*.*")]
            )
            if user_choice:
                wbstego_path = user_choice

        if wbstego_path:
            try:
                subprocess.Popen([wbstego_path], cwd=os.path.dirname(wbstego_path))
                self.log(f"WBStego opened successfully: {wbstego_path}", "SUCCESS", tab="hide")
            except Exception as e:
                self.log(f"Error opening WBStego: {str(e)}", "ERROR", tab="hide")
                messagebox.showerror("Error", f"Failed to open WBStego GUI:\n{str(e)}")
        else:
            self.log("WBStego executable not found.", "ERROR", tab="hide")
            messagebox.showerror("Error", "WBStego executable not found.\nPlease ensure wbStego4.3open.exe is available in the Tools folder or locate it when prompted.")
    
    def create_hide_tab(self, parent):
        """Create Hide tab with text file types"""
        super().create_hide_tab(parent)
        # Update browse buttons for text files
        for widget in parent.winfo_children():
            if isinstance(widget, ttk.Button) and widget.cget("text") == "Browse":
                info = widget.grid_info()
                if info.get("row") == 0:
                    widget.config(command=lambda: self.browse_input_file([
                        ("Text files", "*.txt *.html *.xml"), ("All files", "*.*")
                    ]))
                elif info.get("row") == 1:
                    widget.config(command=lambda: self.browse_output_file([
                        ("Text files", "*.txt *.html *.xml"), ("All files", "*.*")
                    ]))
    
    def create_extract_tab(self, parent):
        """Create Extract tab with text file types"""
        super().create_extract_tab(parent)
        # Update browse button for text files
        for widget in parent.winfo_children():
            if isinstance(widget, ttk.Button) and widget.cget("text") == "Browse":
                widget.config(command=lambda: self.browse_input_file([
                    ("Text files", "*.txt *.html *.xml"), ("All files", "*.*")
                ]))
    
    def hide_message(self):
        """Hide message using WBStego4Open"""
        if not self.validate_inputs(require_message=True, require_password=True, tab="hide"):
            return
        
        self.clear_log("hide")
        self.log("Starting WBStego4Open hide operation...", tab="hide")
        
        try:
            wbstego_path = self.find_wbstego()
            if not wbstego_path:
                self.log("WBStego4Open not found. Please ensure it's installed.", "ERROR", tab="hide")
                messagebox.showerror("Error", "WBStego4Open not found. Please ensure it's installed.")
                return
            
            # Create message file
            msg_file = os.path.join(os.path.dirname(self.output_file.get()), "temp_msg.txt")
            with open(msg_file, "w", encoding="utf-8") as f:
                f.write(self.get_message())
            
            # WBStego encode command (example)
            cmd = [
                wbstego_path,
                "-e",
                "-i", self.input_file.get(),
                "-m", msg_file,
                "-o", self.output_file.get(),
                "-p", self.password.get()
            ]
            
            self.log(f"Running: {' '.join(cmd)}", tab="hide")
            try:
                # Run with the executable's directory as cwd so any relative DLLs/files are found
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60, cwd=os.path.dirname(wbstego_path))
            except Exception as e:
                self.log(f"Exception running WBStego: {e}", "ERROR", tab="hide")
                messagebox.showerror("Error", f"Failed to run WBStego:\n{e}")
                return
            
            if os.path.exists(msg_file):
                os.remove(msg_file)
            
            if result.returncode == 0:
                self.log("Message hidden successfully!", "SUCCESS", tab="hide")
                messagebox.showinfo("Success", f"Message hidden successfully!\nOutput: {self.output_file.get()}")
            else:
                stderr = result.stderr or ""
                self.log(f"Error: {stderr}", "ERROR", tab="hide")
                # Detect common runtime error and offer to open GUI instead
                if "Runtime error 217" in stderr or "Runtime error" in stderr:
                    open_gui = messagebox.askyesno("WBStego runtime error",
                                                   "WBStego crashed with a runtime error while running command-line mode.\nWould you like to open the WBStego GUI instead to perform the operation manually? (Recommended)")
                    if open_gui:
                        try:
                            subprocess.Popen([wbstego_path], cwd=os.path.dirname(wbstego_path))
                        except Exception as e:
                            messagebox.showerror("Error", f"Failed to open WBStego GUI:\n{e}")
                    else:
                        messagebox.showerror("Error", f"Failed to hide message:\n{stderr}")
                else:
                    messagebox.showerror("Error", f"Failed to hide message:\n{stderr}")
        
        except Exception as e:
            self.log(f"Exception: {str(e)}", "ERROR", tab="hide")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def extract_message(self):
        """Extract message using WBStego4Open"""
        if not self.validate_inputs(require_message=False, require_password=True, tab="extract"):
            return
        
        self.clear_log("extract")
        self.log("Starting WBStego4Open extract operation...", tab="extract")
        
        try:
            wbstego_path = self.find_wbstego()
            if not wbstego_path:
                self.log("WBStego4Open not found. Please ensure it's installed.", "ERROR", tab="extract")
                messagebox.showerror("Error", "WBStego4Open not found. Please ensure it's installed.")
                return
            
            msg_file = os.path.join(os.path.dirname(self.input_file.get()), "temp_extracted.txt")
            
            cmd = [
                wbstego_path,
                "-d",
                "-i", self.input_file.get(),
                "-o", msg_file,
                "-p", self.password.get()
            ]
            
            self.log(f"Running: {' '.join(cmd)}", tab="extract")
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60, cwd=os.path.dirname(wbstego_path))
            except Exception as e:
                self.log(f"Exception running WBStego: {e}", "ERROR", tab="extract")
                messagebox.showerror("Error", f"Failed to run WBStego:\n{e}")
                return

            if result.returncode == 0 and os.path.exists(msg_file):
                with open(msg_file, "r", encoding="utf-8") as f:
                    extracted_msg = f.read()
                self.set_message(extracted_msg)
                self.log("Message extracted successfully!", "SUCCESS", tab="extract")
                messagebox.showinfo("Success", "Message extracted successfully!")
                os.remove(msg_file)
            else:
                stderr = result.stderr or ""
                self.log(f"Error: {stderr}", "ERROR", tab="extract")
                if "Runtime error 217" in stderr or "Runtime error" in stderr:
                    open_gui = messagebox.askyesno("WBStego runtime error",
                                                   "WBStego crashed with a runtime error while running command-line mode.\nWould you like to open the WBStego GUI instead to perform the operation manually? (Recommended)")
                    if open_gui:
                        try:
                            subprocess.Popen([wbstego_path], cwd=os.path.dirname(wbstego_path))
                        except Exception as e:
                            messagebox.showerror("Error", f"Failed to open WBStego GUI:\n{e}")
                    else:
                        messagebox.showerror("Error", f"Failed to extract message:\n{stderr}")
                else:
                    messagebox.showerror("Error", f"Failed to extract message:\n{stderr}")
        
        except Exception as e:
            self.log(f"Exception: {str(e)}", "ERROR", tab="extract")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def find_wbstego(self):
        """Find WBStego4Open executable"""
        possible_paths = [
            "wbstego4open",
            "wbstego4open.exe",
            os.path.join(os.path.dirname(__file__), "..", "Tools", "wbstego4open.exe"),
            os.path.join(os.path.dirname(__file__), "..", "tools", "wbs43open-win32", "wbStego4.3open.exe"),
            os.path.join(os.path.dirname(__file__), "..", "Tools", "wbs43open-win32", "wbStego4.3open.exe"),
            os.path.join(os.path.dirname(__file__), "..", "tools", "wbs43open-win32", "wbStego4.3open.exe"),
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
        return None
    


class SToolsTool(BaseToolWindow):
    """S-Tools tool implementation"""
    
    def __init__(self, parent, root_window):
        self.root_window = root_window
        super().__init__(parent, "S-Tools")
    
    def create_hide_tab(self, parent):
        """Create Hide tab with S-Tools file types"""
        super().create_hide_tab(parent)
        # Update browse buttons for S-Tools supported files
        for widget in parent.winfo_children():
            if isinstance(widget, ttk.Button) and widget.cget("text") == "Browse":
                info = widget.grid_info()
                if info.get("row") == 0:
                    widget.config(command=lambda: self.browse_input_file([
                        ("Image files", "*.bmp *.gif"), ("Audio files", "*.wav"), ("All files", "*.*")
                    ]))
                elif info.get("row") == 1:
                    widget.config(command=lambda: self.browse_output_file([
                        ("Image files", "*.bmp *.gif"), ("Audio files", "*.wav"), ("All files", "*.*")
                    ]))
    
    def create_extract_tab(self, parent):
        """Create Extract tab with S-Tools file types"""
        super().create_extract_tab(parent)
        # Update browse button for S-Tools supported files
        for widget in parent.winfo_children():
            if isinstance(widget, ttk.Button) and widget.cget("text") == "Browse":
                widget.config(command=lambda: self.browse_input_file([
                    ("Image files", "*.bmp *.gif"), ("Audio files", "*.wav"), ("All files", "*.*")
                ]))
    
    def open_stools(self):
        """Open S-Tools GUI application"""
        self.clear_log("hide")
        self.log("Opening S-Tools GUI application...", tab="hide")
        
        stools_path = self.find_stools()
        if stools_path:
            try:
                subprocess.Popen([stools_path])
                self.log(f"S-Tools opened successfully: {stools_path}", "SUCCESS", tab="hide")
                messagebox.showinfo("Success", "S-Tools GUI application opened!")
            except Exception as e:
                self.log(f"Error opening S-Tools: {str(e)}", "ERROR", tab="hide")
                messagebox.showerror("Error", f"Failed to open S-Tools:\n{str(e)}")
        else:
            self.log("S-Tools executable not found.", "ERROR", tab="hide")
            messagebox.showerror("Error", "S-Tools executable not found.\nPlease ensure S-Tools.exe is in the Tools directory.")
    
    def hide_message(self):
        """Hide message - Launch GUI tool"""
        self.clear_log("hide")
        self.log("Opening S-Tools GUI application...", tab="hide")
        
        stools_path = self.find_stools()
        if stools_path:
            try:
                subprocess.Popen([stools_path])
                self.log(f"S-Tools opened successfully: {stools_path}", "SUCCESS", tab="hide")
                messagebox.showinfo("Success", "S-Tools GUI application opened!\nUse the application to hide your message.")
            except Exception as e:
                self.log(f"Error opening S-Tools: {str(e)}", "ERROR", tab="hide")
                messagebox.showerror("Error", f"Failed to open S-Tools:\n{str(e)}")
        else:
            self.log("S-Tools executable not found.", "ERROR", tab="hide")
            messagebox.showerror("Error", "S-Tools executable not found.\nPlease ensure S-Tools.exe is in the Tools directory.")
    
    def extract_message(self):
        """Extract message - Launch GUI tool"""
        self.clear_log("extract")
        self.log("Opening S-Tools GUI application...", tab="extract")
        
        stools_path = self.find_stools()
        if stools_path:
            try:
                subprocess.Popen([stools_path])
                self.log(f"S-Tools opened successfully: {stools_path}", "SUCCESS", tab="extract")
                messagebox.showinfo("Success", "S-Tools GUI application opened!\nUse the application to extract your message.")
            except Exception as e:
                self.log(f"Error opening S-Tools: {str(e)}", "ERROR", tab="extract")
                messagebox.showerror("Error", f"Failed to open S-Tools:\n{str(e)}")
        else:
            self.log("S-Tools executable not found.", "ERROR", tab="extract")
            messagebox.showerror("Error", "S-Tools executable not found.\nPlease ensure S-Tools.exe is in the Tools directory.")
    
    def find_stools(self):
        """Find S-Tools executable"""
        possible_paths = [
            os.path.join(os.path.dirname(__file__), "..", "Tools", "S-Tools", "s-tools4", "S-Tools.exe"),
            os.path.join(os.path.dirname(__file__), "..", "tools", "S-Tools", "s-tools4", "S-Tools.exe"),
            "S-Tools.exe",
            "s-tools.exe",
        ]
        for path in possible_paths:
            abs_path = os.path.abspath(path)
            if os.path.exists(abs_path):
                return abs_path
        return None

