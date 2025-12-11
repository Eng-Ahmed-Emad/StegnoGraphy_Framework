"""
Text Steganography Tools
S-Tools and SNOW
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
        
        # S-Tools tab
        stools_frame = ttk.Frame(notebook)
        notebook.add(stools_frame, text="S-Tools")
        self.stools_tool = SToolsTool(stools_frame, self.window)
        
        # SNOW tab
        snow_frame = ttk.Frame(notebook)
        notebook.add(snow_frame, text="SNOW")
        self.snow_tool = SNOWTool(snow_frame, self.window)
        
        # Handle window close event
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_closing(self):
        """Handle window closing event"""
        try:
            # Close the window
            self.window.destroy()
        except Exception:
            pass


class SNOWTool(BaseToolWindow):
    """SNOW (Steganographic Nature Of Whitespace) tool implementation"""
    
    def __init__(self, parent, root_window):
        self.root_window = root_window
        super().__init__(parent, "SNOW")

    def create_hide_tab(self, parent):
        """Create Hide tab for SNOW"""
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
        """Create Extract tab for SNOW"""
        super().create_extract_tab(parent)
        # Update browse button for text files
        for widget in parent.winfo_children():
            if isinstance(widget, ttk.Button) and widget.cget("text") == "Browse":
                widget.config(command=lambda: self.browse_input_file([
                    ("Text files", "*.txt *.html *.xml"), ("All files", "*.*")
                ]))
    
    def hide_message(self):
        """Hide message using SNOW"""
        if not self.validate_inputs(require_message=True, require_password=True, tab="hide"):
            return
        
        self.clear_log("hide")
        self.log("Starting SNOW hide operation...", tab="hide")
        
        try:
            snow_path = self.find_snow()
            if not snow_path:
                self.log("SNOW executable not found.", "ERROR", tab="hide")
                messagebox.showerror("Error", "SNOW executable not found. Please ensure snow.exe is available.")
                return
            
            # Create message file
            msg_file = os.path.join(os.path.dirname(self.output_file.get()), "temp_msg.txt")
            with open(msg_file, "w", encoding="utf-8") as f:
                f.write(self.get_message())
            
            # SNOW encode command
            cmd = [
                snow_path,
                "-C",
                "-p", self.password.get(),
                "-m", msg_file,
                self.input_file.get(),
                self.output_file.get()
            ]
            
            self.log(f"Running: {' '.join(cmd)}", tab="hide")
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            except Exception as e:
                self.log(f"Exception running SNOW: {e}", "ERROR", tab="hide")
                messagebox.showerror("Error", f"Failed to run SNOW:\n{e}")
                return
            
            if os.path.exists(msg_file):
                os.remove(msg_file)
            
            if result.returncode == 0:
                self.log("Message hidden successfully!", "SUCCESS", tab="hide")
                messagebox.showinfo("Success", f"Message hidden successfully!\nOutput: {self.output_file.get()}")
            else:
                stderr = result.stderr or ""
                self.log(f"Error: {stderr}", "ERROR", tab="hide")
                messagebox.showerror("Error", f"Failed to hide message:\n{stderr}")
        
        except Exception as e:
            self.log(f"Exception: {str(e)}", "ERROR", tab="hide")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def extract_message(self):
        """Extract message using SNOW"""
        if not self.validate_inputs(require_message=False, require_password=True, tab="extract"):
            return
        
        self.clear_log("extract")
        self.log("Starting SNOW extract operation...", tab="extract")
        
        try:
            snow_path = self.find_snow()
            if not snow_path:
                self.log("SNOW executable not found.", "ERROR", tab="extract")
                messagebox.showerror("Error", "SNOW executable not found. Please ensure snow.exe is available.")
                return
            
            input_file = self.input_file.get()
            if not os.path.exists(input_file):
                self.log(f"Input file not found: {input_file}", "ERROR", tab="extract")
                messagebox.showerror("Error", f"Input file not found: {input_file}")
                return
            
            # Create temporary file to store extracted message (use absolute path with forward slashes)
            temp_dir = os.path.dirname(os.path.abspath(input_file))
            msg_file = os.path.join(temp_dir, "snow_extracted_msg.txt")
            
            # Convert paths to use forward slashes for consistency
            snow_path_normalized = snow_path.replace("\\", "/")
            input_file_normalized = input_file.replace("\\", "/")
            msg_file_normalized = msg_file.replace("\\", "/")
            
            # SNOW decode command - use -m to specify output message file
            cmd = [
                snow_path_normalized,
                "-C",
                "-Q",
                "-p", self.password.get(),
                "-m", msg_file_normalized,
                input_file_normalized
            ]
            
            self.log(f"SNOW path: {snow_path_normalized}", tab="extract")
            self.log(f"Input file: {input_file_normalized}", tab="extract")
            self.log(f"Output file: {msg_file_normalized}", tab="extract")
            self.log(f"Running: {' '.join(cmd)}", tab="extract")
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                self.log(f"Return code: {result.returncode}", tab="extract")
                
                if result.stdout:
                    self.log(f"Stdout: {result.stdout}", tab="extract")
                if result.stderr:
                    self.log(f"Stderr: {result.stderr}", tab="extract")
                
            except Exception as e:
                self.log(f"Exception running SNOW: {e}", "ERROR", tab="extract")
                messagebox.showerror("Error", f"Failed to run SNOW:\n{e}")
                return

            # Read the extracted message from the file
            if os.path.exists(msg_file):
                try:
                    with open(msg_file, "r", encoding="utf-8") as f:
                        extracted_msg = f.read()
                    
                    # Clean up temp file
                    os.remove(msg_file)
                    
                    if extracted_msg:
                        self.set_message(extracted_msg)
                        self.log(f"Message extracted successfully! Length: {len(extracted_msg)} characters", "SUCCESS", tab="extract")
                        messagebox.showinfo("Success", "Message extracted successfully!")
                    else:
                        self.set_message("")
                        self.log("Message file is empty.", "INFO", tab="extract")
                        messagebox.showinfo("Info", "No message content found.")
                except Exception as e:
                    self.log(f"Error reading extracted message: {e}", "ERROR", tab="extract")
                    messagebox.showerror("Error", f"Failed to read extracted message:\n{e}")
            else:
                # Message file was not created
                self.log(f"Message file was not created at: {msg_file}", "ERROR", tab="extract")
                self.log("This could mean:", "ERROR", tab="extract")
                self.log("1. The password is incorrect", "ERROR", tab="extract")
                self.log("2. The file doesn't contain a valid SNOW-encoded message", "ERROR", tab="extract")
                self.log("3. The input file is corrupted or not readable", "ERROR", tab="extract")
                messagebox.showerror("Error", "Failed to extract message.\n\nNote: Ensure the correct password is used and the file contains a valid SNOW-encoded message.")
        
        except Exception as e:
            self.log(f"Exception: {str(e)}", "ERROR", tab="extract")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    
    def find_snow(self):
        """Find SNOW executable"""
        possible_paths = [
            "snow",
            "snow.exe",
            os.path.join(os.path.dirname(__file__), "..", "snow.exe"),
            os.path.join(os.path.dirname(__file__), "..", "tools", "snow.exe"),
        ]
        
        for path in possible_paths:
            if os.path.isfile(path) and os.access(path, os.X_OK):
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

