"""
Image Steganography Tools
Steghide and Xiao Steganography
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import sys
from .base_tool import BaseToolWindow


class ImageStegoWindow:
    """Window for Image Steganography tools"""
    
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Image Steganography Tools")
        self.window.geometry("750x650")
        
        # Create notebook for tabs
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Steghide tab
        steghide_frame = ttk.Frame(notebook)
        notebook.add(steghide_frame, text="Steghide")
        self.steghide_tool = SteghideTool(steghide_frame, self.window)
        
        # Xiao Steganography tab
        xiao_frame = ttk.Frame(notebook)
        notebook.add(xiao_frame, text="Xiao Steganography")
        self.xiao_tool = XiaoSteganographyTool(xiao_frame, self.window)

        # Open Xiao Steganography immediately when its tab is selected
        def _on_tab_changed(event):
            try:
                selected = notebook.tab(notebook.select(), "text")
                if selected == "Xiao Steganography":
                    # attempt to open the GUI application immediately
                    self.xiao_tool.hide_message()
            except Exception:
                pass

        notebook.bind('<<NotebookTabChanged>>', _on_tab_changed)


class SteghideTool(BaseToolWindow):
    """Steghide tool implementation"""
    
    def __init__(self, parent, root_window):
        self.root_window = root_window
        super().__init__(parent, "Steghide")
    
    def create_hide_tab(self, parent):
        """Create Hide tab with image-specific file types"""
        super().create_hide_tab(parent)
        # Update browse buttons for image files
        for widget in parent.winfo_children():
            if isinstance(widget, ttk.Button) and widget.cget("text") == "Browse":
                # Find which row it's in to determine input vs output
                info = widget.grid_info()
                if info.get("row") == 0:  # Input file browse
                    widget.config(command=lambda: self.browse_input_file([
                        ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"), ("All files", "*.*")
                    ]))
                elif info.get("row") == 1:  # Output file browse
                    widget.config(command=lambda: self.browse_output_file([
                        ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"), ("All files", "*.*")
                    ]))
    
    def create_extract_tab(self, parent):
        """Create Extract tab with image-specific file types"""
        super().create_extract_tab(parent)
        # Update browse button for image files
        for widget in parent.winfo_children():
            if isinstance(widget, ttk.Button) and widget.cget("text") == "Browse":
                widget.config(command=lambda: self.browse_input_file([
                    ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"), ("All files", "*.*")
                ]))
    
    def hide_message(self):
        """Hide message using Steghide"""
        if not self.validate_inputs(require_message=True, require_password=True, tab="hide"):
            return
        
        self.clear_log("hide")
        self.log("Starting Steghide hide operation...", tab="hide")
        
        try:
            steghide_path = self.find_steghide()
            if not steghide_path:
                self.log("Steghide not found. Please ensure steghide.exe is in Tools/steghide/", "ERROR", "hide")
                messagebox.showerror("Error", "Steghide not found. Please ensure steghide.exe is in Tools/steghide/")
                return
            
            # Create message file
            msg_file = os.path.join(os.path.dirname(self.output_file.get()), "temp_msg.txt")
            with open(msg_file, "w", encoding="utf-8") as f:
                f.write(self.get_message())
            
            # Run steghide embed
            cmd = [
                steghide_path,
                "embed",
                "-cf", self.input_file.get(),
                "-ef", msg_file,
                "-sf", self.output_file.get(),
                "-p", self.password.get()
            ]
            
            self.log(f"Running: {' '.join(cmd)}", tab="hide")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            # Clean up temp file
            if os.path.exists(msg_file):
                os.remove(msg_file)
            
            if result.returncode == 0:
                self.log("Message hidden successfully!", "SUCCESS", "hide")
                messagebox.showinfo("Success", f"Message hidden successfully!\nOutput saved to: {self.output_file.get()}")
            else:
                self.log(f"Error: {result.stderr}", "ERROR", "hide")
                messagebox.showerror("Error", f"Failed to hide message:\n{result.stderr}")
        
        except subprocess.TimeoutExpired:
            self.log("Operation timed out", "ERROR", "hide")
            messagebox.showerror("Error", "Operation timed out")
        except Exception as e:
            self.log(f"Exception: {str(e)}", "ERROR", "hide")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def extract_message(self):
        """Extract message using Steghide"""
        if not self.validate_inputs(require_message=False, require_password=True, tab="extract"):
            return
        
        self.clear_log("extract")
        self.log("Starting Steghide extract operation...", tab="extract")
        
        try:
            steghide_path = self.find_steghide()
            if not steghide_path:
                self.log("Steghide not found. Please ensure steghide.exe is in Tools/steghide/", "ERROR", "extract")
                messagebox.showerror("Error", "Steghide not found. Please ensure steghide.exe is in Tools/steghide/")
                return
            
            # Extract to temp file
            msg_file = os.path.join(os.path.dirname(self.input_file.get()), "temp_extracted.txt")
            
            cmd = [
                steghide_path,
                "extract",
                "-sf", self.input_file.get(),
                "-xf", msg_file,
                "-p", self.password.get()
            ]
            
            self.log(f"Running: {' '.join(cmd)}", tab="extract")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and os.path.exists(msg_file):
                with open(msg_file, "r", encoding="utf-8") as f:
                    extracted_msg = f.read()
                self.set_message(extracted_msg)
                self.log("Message extracted successfully!", "SUCCESS", "extract")
                messagebox.showinfo("Success", "Message extracted successfully!")
                os.remove(msg_file)
            else:
                self.log(f"Error: {result.stderr}", "ERROR", "extract")
                messagebox.showerror("Error", f"Failed to extract message:\n{result.stderr}")
        
        except Exception as e:
            self.log(f"Exception: {str(e)}", "ERROR", "extract")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def find_steghide(self):
        """Find steghide executable"""
        # Check Tools folder first
        possible_paths = [
            os.path.join(os.path.dirname(__file__), "steghide", "steghide.exe"),
            os.path.join(os.path.dirname(__file__), "..", "Tools", "steghide", "steghide.exe"),
            os.path.join(os.path.dirname(__file__), "..", "tools", "steghide", "steghide.exe"),
            os.path.join(os.path.dirname(__file__), "..", "Tools", "steghide.exe"),
            "steghide.exe",
            "steghide",
        ]
        
        for path in possible_paths:
            abs_path = os.path.abspath(path)
            if os.path.exists(abs_path):
                return abs_path
        
        # Check if command exists in PATH
        for cmd in ["steghide", "steghide.exe"]:
            if self.command_exists(cmd):
                return cmd
        return None
    
    def command_exists(self, cmd):
        """Check if command exists in PATH"""
        try:
            subprocess.run([cmd, "--version"], capture_output=True, timeout=2)
            return True
        except:
            return False
    


class XiaoSteganographyTool(BaseToolWindow):
    """Xiao Steganography tool implementation"""
    
    def __init__(self, parent, root_window):
        self.root_window = root_window
        super().__init__(parent, "Xiao Steganography")
    
    def create_hide_tab(self, parent):
        """Create Hide tab"""
        super().create_hide_tab(parent)
        # Update browse buttons for image files
        for widget in parent.winfo_children():
            if isinstance(widget, ttk.Button) and widget.cget("text") == "Browse":
                info = widget.grid_info()
                if info.get("row") == 0:
                    widget.config(command=lambda: self.browse_input_file([
                        ("Image files", "*.jpg *.jpeg *.png *.bmp"), ("All files", "*.*")
                    ]))
                elif info.get("row") == 1:
                    widget.config(command=lambda: self.browse_output_file([
                        ("Image files", "*.jpg *.jpeg *.png *.bmp"), ("All files", "*.*")
                    ]))
    
    def create_extract_tab(self, parent):
        """Create Extract tab"""
        super().create_extract_tab(parent)
        # Update browse button for image files
        for widget in parent.winfo_children():
            if isinstance(widget, ttk.Button) and widget.cget("text") == "Browse":
                widget.config(command=lambda: self.browse_input_file([
                    ("Image files", "*.jpg *.jpeg *.png *.bmp"), ("All files", "*.*")
                ]))
    
    def find_xiao_steganography(self):
        """Find Xiao Steganography executable"""
        possible_paths = [
            os.path.join(os.path.dirname(__file__), "Xiao Stenography.lnk"),
            os.path.join(os.path.dirname(__file__), "..", "Tools", "Xiao Stenography.lnk"),
            os.path.join(os.path.dirname(__file__), "..", "tools", "Xiao Stenography.lnk"),
            os.path.join(os.path.dirname(__file__), "..", "Tools", "XiaoSteganography.exe"),
            os.path.join(os.path.dirname(__file__), "..", "Tools", "Xiao.exe"),
            "XiaoSteganography.exe",
            "Xiao.exe",
        ]
        for path in possible_paths:
            abs_path = os.path.abspath(path)
            if os.path.exists(abs_path):
                return abs_path
        return None
    
    def hide_message(self):
        """Hide message - Launch GUI tool"""
        self.clear_log("hide")
        self.log("Opening Xiao Steganography GUI application...", tab="hide")
        
        xiao_path = self.find_xiao_steganography()
        if xiao_path:
            try:
                # Handle .lnk files on Windows - use shell=True to let Windows handle it
                subprocess.Popen([xiao_path], shell=True)
                self.log(f"Xiao Steganography opened successfully: {xiao_path}", "SUCCESS", tab="hide")
                messagebox.showinfo("Success", "Xiao Steganography GUI application opened!\nUse the application to hide your message.")
            except Exception as e:
                self.log(f"Error opening Xiao Steganography: {str(e)}", "ERROR", tab="hide")
                messagebox.showerror("Error", f"Failed to open Xiao Steganography:\n{str(e)}")
        else:
            self.log("Xiao Steganography executable not found.", "ERROR", tab="hide")
            messagebox.showerror("Error", "Xiao Steganography executable not found.\nPlease ensure it's in the Tools directory.")
    
    def extract_message(self):
        """Extract message - Launch GUI tool"""
        self.clear_log("extract")
        self.log("Opening Xiao Steganography GUI application...", tab="extract")
        
        xiao_path = self.find_xiao_steganography()
        if xiao_path:
            try:
                subprocess.Popen([xiao_path], shell=True)
                self.log(f"Xiao Steganography opened successfully: {xiao_path}", "SUCCESS", tab="extract")
                messagebox.showinfo("Success", "Xiao Steganography GUI application opened!\nUse the application to extract your message.")
            except Exception as e:
                self.log(f"Error opening Xiao Steganography: {str(e)}", "ERROR", tab="extract")
                messagebox.showerror("Error", f"Failed to open Xiao Steganography:\n{str(e)}")
        else:
            self.log("Xiao Steganography executable not found.", "ERROR", tab="extract")
            messagebox.showerror("Error", "Xiao Steganography executable not found.\nPlease ensure it's in the Tools directory.")

