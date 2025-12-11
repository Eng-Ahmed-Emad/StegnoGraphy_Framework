"""
ADS (Alternate Data Streams) Tools
Streams and ADS Viewer
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
from .base_tool import BaseToolWindow


class ADSToolsWindow:
    """Window for ADS Tools"""
    
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("ADS Tools")
        self.window.geometry("750x650")
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Streams tab
        streams_frame = ttk.Frame(notebook)
        notebook.add(streams_frame, text="Streams")
        self.streams_tool = StreamsTool(streams_frame, self.window)
        
        # ADS Viewer tab
        adsviewer_frame = ttk.Frame(notebook)
        notebook.add(adsviewer_frame, text="ADS Viewer")
        self.adsviewer_tool = ADSViewerTool(adsviewer_frame, self.window)


class StreamsTool(BaseToolWindow):
    """Streams tool implementation"""
    
    def __init__(self, parent, root_window):
        self.root_window = root_window
        self.stream_name = tk.StringVar(value="hidden")
        super().__init__(parent, "Streams")
    
    def create_hide_tab(self, parent):
        """Create Hide tab with stream name field"""
        super().create_hide_tab(parent)
        # Add stream name field after password
        # Find password row and insert stream name after it
        for i, widget in enumerate(parent.winfo_children()):
            if isinstance(widget, ttk.Entry) and widget.cget("show") == "*":
                # Password field found, add stream name after it
                info = widget.grid_info()
                row = info.get("row", 3)
                
                # Insert stream name label and entry
                ttk.Label(parent, text="Stream Name:", font=("Arial", 10)).grid(
                    row=row+1, column=0, sticky=tk.W, pady=5
                )
                stream_entry = ttk.Entry(parent, textvariable=self.stream_name, width=50)
                stream_entry.grid(row=row+1, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)
                
                # Move hide button down
                for btn in parent.winfo_children():
                    if isinstance(btn, ttk.Button) and btn.cget("text") == "Hide Message":
                        btn_info = btn.grid_info()
                        btn.grid(row=int(btn_info.get("row", 4))+1, column=btn_info.get("column", 0), 
                                columnspan=btn_info.get("columnspan", 3), pady=btn_info.get("pady", 20))
                
                # Move log area down
                for log in parent.winfo_children():
                    if isinstance(log, tk.Text) and log.cget("state") == "disabled":
                        log_info = log.grid_info()
                        log.grid(row=int(log_info.get("row", 5))+1, column=log_info.get("column", 0),
                                columnspan=log_info.get("columnspan", 3), sticky=log_info.get("sticky", (tk.W, tk.E, tk.N, tk.S)),
                                padx=log_info.get("padx", 5), pady=log_info.get("pady", 5))
                break
        
        # Update browse buttons
        for widget in parent.winfo_children():
            if isinstance(widget, ttk.Button) and widget.cget("text") == "Browse":
                info = widget.grid_info()
                if info.get("row") == 0:
                    widget.config(command=lambda: self.browse_input_file([
                        ("All files", "*.*")
                    ]))
                elif info.get("row") == 1:
                    widget.config(command=lambda: self.browse_output_file([
                        ("All files", "*.*")
                    ]))
    
    def create_extract_tab(self, parent):
        """Create Extract tab with stream name field"""
        super().create_extract_tab(parent)
        # Add stream name field after password
        for i, widget in enumerate(parent.winfo_children()):
            if isinstance(widget, ttk.Entry) and widget.cget("show") == "*":
                info = widget.grid_info()
                row = info.get("row", 1)
                
                ttk.Label(parent, text="Stream Name:", font=("Arial", 10)).grid(
                    row=row+1, column=0, sticky=tk.W, pady=5
                )
                stream_entry = ttk.Entry(parent, textvariable=self.stream_name, width=50)
                stream_entry.grid(row=row+1, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)
                
                # Move extract button and other widgets down
                for btn in parent.winfo_children():
                    if isinstance(btn, ttk.Button) and btn.cget("text") == "Extract Message":
                        btn_info = btn.grid_info()
                        btn.grid(row=int(btn_info.get("row", 2))+1, column=btn_info.get("column", 0),
                                columnspan=btn_info.get("columnspan", 3), pady=btn_info.get("pady", 20))
                break
        
        # Add List Streams button
        for widget in parent.winfo_children():
            if isinstance(widget, ttk.Button) and widget.cget("text") == "Extract Message":
                info = widget.grid_info()
                list_btn = ttk.Button(parent, text="List Streams", command=self.list_streams, width=25)
                list_btn.grid(row=int(info.get("row", 2))+1, column=0, columnspan=3, pady=10)
                break
        
        # Update browse button
        for widget in parent.winfo_children():
            if isinstance(widget, ttk.Button) and widget.cget("text") == "Browse":
                widget.config(command=lambda: self.browse_input_file([
                    ("All files", "*.*")
                ]))
    
    def hide_message(self):
        """Hide message in ADS"""
        if not self.input_file.get():
            messagebox.showerror("Error", "Please select a file to hide message in.")
            return
        
        if not os.path.exists(self.input_file.get()):
            messagebox.showerror("Error", "File does not exist.")
            return
        
        if not self.get_message():
            messagebox.showerror("Error", "Please enter a secret message.")
            return
        
        self.clear_log("hide")
        self.log("Starting ADS hide operation...", tab="hide")
        
        try:
            file_path = self.input_file.get()
            stream_name = self.stream_name.get()
            
            if not stream_name:
                messagebox.showerror("Error", "Please enter a stream name.")
                return
            
            # Create stream file path
            stream_path = f"{file_path}:{stream_name}"
            
            # Write message to ADS
            try:
                with open(stream_path, "w", encoding="utf-8") as f:
                    f.write(self.get_message())
                
                self.log(f"Message hidden successfully in stream: {stream_path}", "SUCCESS", tab="hide")
                self.log(f"File: {file_path}", tab="hide")
                self.log(f"Stream: {stream_name}", tab="hide")
                messagebox.showinfo("Success", f"Message hidden successfully!\nStream: {stream_path}")
            
            except Exception as e:
                self.log(f"Error writing to ADS: {str(e)}", "ERROR", tab="hide")
                self.log("Note: ADS is only supported on NTFS file systems.", "INFO", tab="hide")
                messagebox.showerror("Error", f"Failed to write to ADS:\n{str(e)}\n\nNote: ADS is only supported on NTFS file systems.")
        
        except Exception as e:
            self.log(f"Exception: {str(e)}", "ERROR", tab="hide")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def extract_message(self):
        """Extract message from ADS"""
        if not self.validate_inputs(require_message=False, require_password=False, tab="extract"):
            return
        
        self.clear_log("extract")
        self.log("Starting ADS extract operation...", tab="extract")
        
        try:
            file_path = self.input_file.get()
            stream_name = self.stream_name.get()
            
            if not stream_name:
                messagebox.showerror("Error", "Please enter a stream name.")
                return
            
            stream_path = f"{file_path}:{stream_name}"
            
            # Read from ADS
            try:
                with open(stream_path, "r", encoding="utf-8") as f:
                    extracted_msg = f.read()
                
                self.set_message(extracted_msg)
                self.log(f"Message extracted successfully from stream: {stream_path}", "SUCCESS", tab="extract")
                self.log(f"File: {file_path}", tab="extract")
                self.log(f"Stream: {stream_name}", tab="extract")
                messagebox.showinfo("Success", "Message extracted successfully!")
            
            except FileNotFoundError:
                self.log(f"Stream not found: {stream_path}", "ERROR", tab="extract")
                messagebox.showerror("Error", f"Stream not found: {stream_path}")
            except Exception as e:
                self.log(f"Error reading from ADS: {str(e)}", "ERROR", tab="extract")
                messagebox.showerror("Error", f"Failed to read from ADS:\n{str(e)}")
        
        except Exception as e:
            self.log(f"Exception: {str(e)}", "ERROR", tab="extract")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def list_streams(self):
        """List all streams in a file"""
        if not self.input_file.get() or not os.path.exists(self.input_file.get()):
            messagebox.showerror("Error", "Please select a valid file.")
            return
        
        self.clear_log("extract")
        self.log("Listing streams...", tab="extract")
        
        try:
            streams_path = self.find_streams()
            file_path = self.input_file.get()
            
            if streams_path:
                # Use Sysinternals Streams tool
                cmd = [streams_path, "-s", file_path]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10, shell=True)
                
                if result.returncode == 0:
                    self.log(result.stdout, "INFO", tab="extract")
                else:
                    self.log(result.stderr, "ERROR", tab="extract")
            else:
                # Manual listing (simplified)
                self.log(f"File: {file_path}", "INFO", tab="extract")
                self.log("Note: Install Sysinternals Streams tool for detailed stream listing.", "INFO", tab="extract")
                self.log("You can manually check streams by trying to read them.", "INFO", tab="extract")
        
        except Exception as e:
            self.log(f"Exception: {str(e)}", "ERROR", tab="extract")
    
    def find_streams(self):
        """Find Streams executable"""
        possible_paths = [
            "streams.exe",
            "Streams.exe",
            os.path.join(os.path.dirname(__file__), "..", "Tools", "streams.exe"),
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
        return None


class ADSViewerTool(BaseToolWindow):
    """ADS Viewer tool implementation"""
    
    def __init__(self, parent, root_window):
        self.root_window = root_window
        super().__init__(parent, "ADS Viewer")
    
    def create_hide_tab(self, parent):
        """Create Hide tab"""
        super().create_hide_tab(parent)
        # Update browse buttons
        for widget in parent.winfo_children():
            if isinstance(widget, ttk.Button) and widget.cget("text") == "Browse":
                info = widget.grid_info()
                if info.get("row") == 0:
                    widget.config(command=lambda: self.browse_input_file([
                        ("All files", "*.*")
                    ]))
                elif info.get("row") == 1:
                    widget.config(command=lambda: self.browse_output_file([
                        ("All files", "*.*")
                    ]))
    
    def create_extract_tab(self, parent):
        """Create Extract tab"""
        super().create_extract_tab(parent)
        # Update browse button
        for widget in parent.winfo_children():
            if isinstance(widget, ttk.Button) and widget.cget("text") == "Browse":
                widget.config(command=lambda: self.browse_input_file([
                    ("All files", "*.*")
                ]))
    
    def find_ads_viewer(self):
        """Find ADS Viewer executable"""
        possible_paths = [
            os.path.join(os.path.dirname(__file__), "..", "Tools", "ADSViewer.exe"),
            os.path.join(os.path.dirname(__file__), "..", "tools", "ADSViewer.exe"),
            os.path.join(os.path.dirname(__file__), "..", "tools", "ADS Viewer.exe"),
            os.path.join(os.path.dirname(__file__), "..", "Tools", "ADSViewer", "ADSViewer.exe"),
            "ADSViewer.exe",
            "adsviewer.exe",
        ]
        for path in possible_paths:
            abs_path = os.path.abspath(path)
            if os.path.exists(abs_path):
                return abs_path
        return None
    
    def view_ads(self):
        """View ADS for selected file - Launch GUI tool"""
        self.clear_log("extract")
        self.log("Opening ADS Viewer GUI application...", tab="extract")
        
        adsviewer_path = self.find_ads_viewer()
        if adsviewer_path:
            try:
                subprocess.Popen([adsviewer_path])
                self.log(f"ADS Viewer opened successfully: {adsviewer_path}", "SUCCESS", tab="extract")
                messagebox.showinfo("Success", "ADS Viewer GUI application opened!\nUse the application to view and manage ADS.")
            except Exception as e:
                self.log(f"Error opening ADS Viewer: {str(e)}", "ERROR", tab="extract")
                messagebox.showerror("Error", f"Failed to open ADS Viewer:\n{str(e)}")
        else:
            self.log("ADS Viewer executable not found.", "ERROR", tab="extract")
            messagebox.showerror("Error", "ADS Viewer executable not found.\nPlease ensure ADSViewer.exe is in the Tools directory.")
    
    def hide_message(self):
        """Hide message - Launch GUI tool"""
        if not self.input_file.get():
            messagebox.showerror("Error", "Please select a file.")
            return
        
        if not os.path.exists(self.input_file.get()):
            messagebox.showerror("Error", "File does not exist.")
            return
        
        self.clear_log("hide")
        self.log("Opening ADS Viewer GUI application...", tab="hide")
        
        adsviewer_path = self.find_ads_viewer()
        if adsviewer_path:
            try:
                subprocess.Popen([adsviewer_path])
                self.log(f"ADS Viewer opened successfully: {adsviewer_path}", "SUCCESS", tab="hide")
                messagebox.showinfo("Success", "ADS Viewer GUI application opened!\nUse the application to hide messages.")
            except Exception as e:
                self.log(f"Error opening ADS Viewer: {str(e)}", "ERROR", tab="hide")
                messagebox.showerror("Error", f"Failed to open ADS Viewer:\n{str(e)}")
        else:
            self.log("ADS Viewer executable not found.", "ERROR", tab="hide")
            messagebox.showerror("Error", "ADS Viewer executable not found.\nPlease ensure ADSViewer.exe is in the Tools directory.")
    
    def extract_message(self):
        """Extract message - Launch GUI tool"""
        if not self.input_file.get():
            messagebox.showerror("Error", "Please select a file.")
            return
        
        if not os.path.exists(self.input_file.get()):
            messagebox.showerror("Error", "File does not exist.")
            return
        
        self.clear_log("extract")
        self.log("Opening ADS Viewer GUI application...", tab="extract")
        
        adsviewer_path = self.find_ads_viewer()
        if adsviewer_path:
            try:
                subprocess.Popen([adsviewer_path])
                self.log(f"ADS Viewer opened successfully: {adsviewer_path}", "SUCCESS", tab="extract")
                messagebox.showinfo("Success", "ADS Viewer GUI application opened!\nUse the application to extract messages.")
            except Exception as e:
                self.log(f"Error opening ADS Viewer: {str(e)}", "ERROR", tab="extract")
                messagebox.showerror("Error", f"Failed to open ADS Viewer:\n{str(e)}")
        else:
            self.log("ADS Viewer executable not found.", "ERROR", tab="extract")
            messagebox.showerror("Error", "ADS Viewer executable not found.\nPlease ensure ADSViewer.exe is in the Tools directory.")

