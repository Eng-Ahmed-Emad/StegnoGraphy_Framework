"""
Video/GIF Steganography Tools
GIF Shuffle Tool
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import os
from .base_tool import BaseToolWindow, find_executable, launch_executable


class VideoStegoWindow:
    """Window for Video/GIF Steganography tools"""
    
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Video/GIF Steganography Tools")
        self.window.geometry("750x650")
        
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # GIF Shuffle Tool tab
        gif_frame = ttk.Frame(notebook)
        notebook.add(gif_frame, text="GIF Shuffle Tool")
        self.gif_tool = GIFShuffleTool(gif_frame, self.window)
        
        # DeEgger Embedder GUI launcher tab
        deegger_frame = ttk.Frame(notebook)
        notebook.add(deegger_frame, text="DeEgger Embedder")
        self.deegger_tool = DeEggerTool(deegger_frame, self.window)

        # Auto-launch DeEgger when its tab is selected
        def _on_video_tab_changed(event):
            try:
                selected = notebook.tab(notebook.select(), "text")
                if selected == "DeEgger Embedder":
                    self.deegger_tool.launch_deegger()
            except Exception:
                pass

        notebook.bind('<<NotebookTabChanged>>', _on_video_tab_changed)


class GIFShuffleTool(BaseToolWindow):
    """GIF Shuffle Tool implementation"""
    
    def __init__(self, parent, root_window):
        self.root_window = root_window
        super().__init__(parent, "GIF Shuffle Tool")
    
    def create_hide_tab(self, parent):
        """Create Hide tab with GIF file types"""
        super().create_hide_tab(parent)
        # Update browse buttons for GIF files
        for widget in parent.winfo_children():
            if isinstance(widget, ttk.Button) and widget.cget("text") == "Browse":
                info = widget.grid_info()
                if info.get("row") == 0:
                    widget.config(command=lambda: self.browse_input_file([
                        ("GIF files", "*.gif"), ("All files", "*.*")
                    ]))
                elif info.get("row") == 1:
                    widget.config(command=lambda: self.browse_output_file([
                        ("GIF files", "*.gif"), ("All files", "*.*")
                    ]))
    
    def create_extract_tab(self, parent):
        """Create Extract tab with GIF file types"""
        super().create_extract_tab(parent)
        # Update browse button for GIF files
        for widget in parent.winfo_children():
            if isinstance(widget, ttk.Button) and widget.cget("text") == "Browse":
                widget.config(command=lambda: self.browse_input_file([
                    ("GIF files", "*.gif"), ("All files", "*.*")
                ]))
    
    def hide_message(self):
        """Hide message using GIF Shuffle Tool"""
        if not self.validate_inputs(require_message=True, require_password=False, tab="hide"):
            return
        
        self.clear_log("hide")
        self.log("Starting GIF Shuffle Tool hide operation...", tab="hide")
        
        try:
            gifshuf_path = self.find_gifshuf()
            if not gifshuf_path:
                messagebox.showerror("Error", "GIFSHUF.EXE not found. Please ensure it's in the Tools directory.")
                return
            
            message = self.get_message()
            password = self.password.get() or ""
            
            # GIF Shuffle Tool hide command: -CS -m message -p password input output
            cmd = [
                gifshuf_path,
                '-CS',
                '-m',
                message,
                '-p',
                password,
                self.input_file.get(),
                self.output_file.get(),
            ]
            
            self.log(f"Running: {' '.join(cmd)}", tab="hide")
            subprocess.Popen(cmd)
            self.log("Message hidden successfully!", "SUCCESS", "hide")
            messagebox.showinfo("Success", f"Message hidden successfully!\nOutput: {self.output_file.get()}")
        
        except Exception as e:
            self.log(f"Exception: {str(e)}", "ERROR", "hide")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def extract_message(self):
        """Extract message using GIF Shuffle Tool"""
        if not self.validate_inputs(require_message=False, require_password=False, tab="extract"):
            return
        
        self.clear_log("extract")
        self.log("Starting GIF Shuffle Tool extract operation...", tab="extract")
        
        try:
            gifshuf_path = self.find_gifshuf()
            if not gifshuf_path:
                messagebox.showerror("Error", "GIFSHUF.EXE not found. Please ensure it's in the Tools directory.")
                return
            
            password = self.password.get() or ""
            
            # GIF Shuffle Tool extract command: -C -p password input
            cmd = [
                gifshuf_path,
                '-C',
                '-p',
                password,
                self.input_file.get(),
            ]

            self.log(f"Running: {' '.join(cmd)}", tab="extract")
            # Run the tool with its executable directory as cwd so relative paths resolve
            run = subprocess.run(cmd, capture_output=True, timeout=60, cwd=os.path.dirname(gifshuf_path))

            # If the tool returned a non-zero exit code, show stderr
            if run.returncode != 0:
                stderr = run.stderr.decode(errors='replace') if run.stderr else ''
                self.log(f"GIF Shuffle failed: {stderr}", "ERROR", "extract")
                messagebox.showerror("Error", f"Extraction failed:\n{stderr}")
                return

            stdout_bytes = run.stdout or b''
            if not stdout_bytes:
                self.log("No message found or extraction returned empty output.", "ERROR", "extract")
                messagebox.showwarning("Warning", "No message found or extraction returned empty output.")
                return

            # Heuristic checks to avoid showing gibberish when password is wrong.
            total = len(stdout_bytes)
            printable = 0
            alnum_space = 0
            for b in stdout_bytes:
                if b in (9, 10, 13) or 32 <= b <= 126:
                    printable += 1
                # letters, digits, and whitespace are good indicators of readable text
                if b in (9, 10, 13) or 32 <= b <= 126 and (
                    48 <= b <= 57 or 65 <= b <= 90 or 97 <= b <= 122 or b == 32
                ):
                    alnum_space += 1
            printable_ratio = printable / total if total > 0 else 0
            alnum_space_ratio = alnum_space / total if total > 0 else 0

            # Decide thresholds: require majority printable and at least some alphanumeric content
            if printable_ratio < 0.7 or alnum_space_ratio < 0.35:
                # Probably binary/gibberish (wrong password). Don't display binary data.
                self.log("Extraction returned non-text output — likely wrong password.", "ERROR", "extract")
                # Offer to save raw output for advanced users
                save_raw = messagebox.askyesno("Possible wrong password",
                                               "Extraction produced non-text output (likely wrong password).\nDo you want to save the raw output to a file for inspection?")
                if save_raw:
                    try:
                        default_path = os.path.join(os.path.dirname(self.input_file.get()), "gifshuf_raw_output.bin")
                        with open(default_path, "wb") as wf:
                            wf.write(stdout_bytes)
                        messagebox.showinfo("Saved", f"Raw output saved to:\n{default_path}")
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to save raw output:\n{str(e)}")
                return

            # Safe to decode and show
            output_text = stdout_bytes.decode(errors='replace')
            self.set_message(output_text)
            self.log("Message extracted successfully!", "SUCCESS", "extract")
            self.log(f"Extracted message: {output_text}", tab="extract")
            messagebox.showinfo("Success", "Message extracted successfully!")
        
        except Exception as e:
            self.log(f"Exception: {str(e)}", "ERROR", "extract")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def find_gifshuf(self):
        """Find GIFShuf executable"""
        possible_paths = [
            os.path.join(os.path.dirname(__file__), "GIFShuff-Tool", "GIFSHUF.EXE"),
            os.path.join(os.path.dirname(__file__), "GIFShuff-Tool", "GIFSHUF.exe"),
            os.path.join(os.path.dirname(__file__), "..", "Tools", "GIFShuff-Tool", "GIFSHUF.EXE"),
            os.path.join(os.path.dirname(__file__), "..", "tools", "GIFShuff-Tool", "GIFSHUF.EXE"),
            os.path.join(os.path.dirname(__file__), "..", "Tools", "GIFShuff-Tool", "GIFSHUF.exe"),
            os.path.join(os.path.dirname(__file__), "..", "Tools", "GIFSHUF.EXE"),
            "GIFSHUF.EXE",
            "GIFSHUF.exe",
            "gifshuf.exe",
        ]
        for path in possible_paths:
            abs_path = os.path.abspath(path)
            if os.path.exists(abs_path):
                return abs_path
        return None


    # HideItPro tool removed from project


class DeEggerTool:
    """Simple launcher for the DeEgger Embedder GUI."""

    def __init__(self, parent, root_window):
        self.parent = parent
        self.root_window = root_window

        lbl = ttk.Label(parent, text="DeEgger Embedder Launcher", font=(None, 11, "bold"))
        lbl.pack(anchor="w", padx=10, pady=(8, 4))

        info = ttk.Label(parent, text="Launch the DeEgger Embedder GUI application.")
        info.pack(anchor="w", padx=10, pady=(0, 8))

        btn = ttk.Button(parent, text="Launch DeEgger Embedder", command=self.launch_deegger)
        btn.pack(anchor="w", padx=10, pady=(0, 8))

    def launch_deegger(self):
        # Try detected or packaged paths first
        deegger_path = self.find_deegger()

        def try_open(path):
            ok = launch_executable(path)
            if ok:
                messagebox.showinfo("Success", "DeEgger GUI application opened!\nUse the application to hide or extract messages.")
            else:
                messagebox.showerror("Error", f"Failed to open DeEgger: \n{path}")
            return ok

        if deegger_path and try_open(deegger_path):
            return

        # If not found, ask the user to locate the exe or shortcut
        user_choice = filedialog.askopenfilename(
            title="Locate DeEgger executable",
            initialdir=os.path.abspath(os.path.join(os.path.dirname(__file__), '..')),
            filetypes=[("Executables", "*.exe;*.lnk"), ("All files", "*.*")]
        )
        if user_choice:
            try_open(user_choice)

    def find_deegger(self):
        """Find DeEgger executable or shortcut"""
        possible_paths = [
            os.path.join(os.path.dirname(__file__), "DeEgger Embedder.lnk"),
            os.path.join(os.path.dirname(__file__), "DeEgger Embedder.exe"),
            os.path.join(os.path.dirname(__file__), "DeEgger Embedder.exe.lnk"),
            os.path.join(os.path.dirname(__file__), "..", "Tools", "DeEgger Embedder.exe"),
            os.path.join(os.path.dirname(__file__), "..", "Tools", "DeEgger Embedder.lnk"),
            os.path.join(os.path.dirname(__file__), "..", "tools", "DeEgger Embedder.exe"),
            os.path.join(os.path.dirname(__file__), "..", "tools", "DeEgger Embedder.lnk"),
            os.path.join(os.path.dirname(__file__), "..", "Tools", "DeEgger Embedder", "DeEgger Embedder.exe"),
            "DeEgger Embedder.exe",
            "DeEgger Embedder.lnk",
            "deegger embedder.exe",
            "deegger.exe",
        ]
        return find_executable(possible_paths)
        return find_executable(possible_paths)

