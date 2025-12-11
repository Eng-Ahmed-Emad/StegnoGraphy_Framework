"""
Audio Steganography Tools
MP3Stego and DeepSound
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import os
from .base_tool import BaseToolWindow


class AudioStegoWindow:
    """Window for Audio Steganography tools"""
    
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Audio Steganography Tools")
        self.window.geometry("750x650")
        
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # MP3Stego tab
        mp3_frame = ttk.Frame(notebook)
        notebook.add(mp3_frame, text="MP3Stego")
        self.mp3_tool = MP3StegoTool(mp3_frame, self.window)
        
        
        # DeepSound tab
        deepsound_frame = ttk.Frame(notebook)
        notebook.add(deepsound_frame, text="DeepSound")
        self.deepsound_tool = DeepSoundTool(deepsound_frame, self.window)

        # Open DeepSound immediately when its tab is selected
        def _on_tab_changed(event):
            try:
                selected = notebook.tab(notebook.select(), "text")
                if selected == "DeepSound":
                    # attempt to open the GUI immediately
                    self.deepsound_tool.hide_message()
            except Exception:
                pass

        notebook.bind('<<NotebookTabChanged>>', _on_tab_changed)


class MP3StegoTool(BaseToolWindow):
    """MP3Stego tool implementation"""
    
    def __init__(self, parent, root_window):
        self.root_window = root_window
        super().__init__(parent, "MP3Stego")
    
    def create_hide_tab(self, parent):
        """Create Hide tab for MP3Stego. MP3Stego expects a WAV input and
        produces an MP3 output, so offer WAV as the input filter and MP3 for
        the output to avoid users selecting an unsupported format by mistake.
        """
        super().create_hide_tab(parent)
        # Update browse buttons: input should be WAV (uncompressed), output MP3
        for widget in parent.winfo_children():
            if isinstance(widget, ttk.Button) and widget.cget("text") == "Browse":
                info = widget.grid_info()
                if info.get("row") == 0:
                    # Input should be WAV (MP3Stego encodes during compression)
                    widget.config(command=lambda: self.browse_input_file([
                        ("WAV files", "*.wav"), ("All files", "*.*")
                    ]))
                elif info.get("row") == 1:
                    # Output is MP3
                    widget.config(command=lambda: self.browse_output_file([
                        ("MP3 files", "*.mp3"), ("All files", "*.*")
                    ]))
    
    def create_extract_tab(self, parent):
        """Create Extract tab with MP3 file types"""
        super().create_extract_tab(parent)
        # Update browse button for MP3 files
        for widget in parent.winfo_children():
            if isinstance(widget, ttk.Button) and widget.cget("text") == "Browse":
                widget.config(command=lambda: self.browse_input_file([
                    ("MP3 files", "*.mp3"), ("All files", "*.*")
                ]))
    
    def hide_message(self):
        """Hide message using MP3Stego"""
        if not self.validate_inputs(require_message=True, require_password=True, tab="hide"):
            return
        
        self.clear_log("hide")
        self.log("Starting MP3Stego hide operation...", tab="hide")
        
        try:
            mp3stego_path = self.find_mp3stego()
            if not mp3stego_path:
                self.log("MP3Stego Encode.exe not found. Please ensure it's in Tools/MP3Stego/", "ERROR", "hide")
                messagebox.showerror("Error", "MP3Stego Encode.exe not found. Please ensure it's in Tools/MP3Stego/")
                return
            # MP3Stego expects a WAV input file (the encoder compresses WAV -> MP3 while
            # embedding the data). Prevent confusing errors by checking the extension
            input_path = self.input_file.get()
            if not input_path.lower().endswith('.wav'):
                self.log("MP3Stego requires a WAV input file. Please convert your audio to WAV.", "ERROR", "hide")
                messagebox.showerror("Error", "MP3Stego requires a WAV input file (uncompressed).\nPlease convert your audio to WAV and try again.")
                return
            
            # Create message file
            msg_file = os.path.join(os.path.dirname(self.output_file.get()), "temp_msg.txt")
            with open(msg_file, "w", encoding="utf-8") as f:
                f.write(self.get_message())
            
            # MP3Stego encode command
            # Use correct MP3Stego flags: -E <filename> and -P <pass>
            # README example: encode -E data.txt -P pass sound.wav sound.mp3
            cmd = [
                mp3stego_path,
                "-E", msg_file,
                "-P", self.password.get(),
                self.input_file.get(),
                self.output_file.get()
            ]
            
            self.log(f"Running: {' '.join(cmd)}", tab="hide")
            # MP3Stego requires access to its local 'tables' directory. Run
            # the encoder with its executable directory as the working dir so
            # relative paths like './tables/' resolve correctly.
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
                cwd=os.path.dirname(mp3stego_path)
            )
            
            if os.path.exists(msg_file):
                os.remove(msg_file)
            
            if result.returncode == 0:
                self.log("Message hidden successfully!", "SUCCESS", "hide")
                messagebox.showinfo("Success", f"Message hidden successfully!\nOutput: {self.output_file.get()}")
            else:
                self.log(f"Error: {result.stderr}", "ERROR", "hide")
                messagebox.showerror("Error", f"Failed to hide message:\n{result.stderr}")
        
        except Exception as e:
            self.log(f"Exception: {str(e)}", "ERROR", "hide")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def extract_message(self):
        """Extract message using MP3Stego"""
        if not self.validate_inputs(require_message=False, require_password=True, tab="extract"):
            return
        
        self.clear_log("extract")
        self.log("Starting MP3Stego extract operation...", tab="extract")
        
        try:
            decode_path = self.find_mp3stego_decode()
            if not decode_path:
                self.log("MP3Stego Decode.exe not found. Please ensure it's in Tools/MP3Stego/", "ERROR", "extract")
                messagebox.showerror("Error", "MP3Stego Decode.exe not found. Please ensure it's in Tools/MP3Stego/")
                return
            
            msg_file = os.path.join(os.path.dirname(self.input_file.get()), "temp_extracted.txt")
            
            # MP3Stego Decode.exe command format
            # Use correct decode invocation: decode -X -P <pass> <infile>
            # MP3Stego will create a file named <infile>.txt containing the hidden data
            cmd = [
                decode_path,
                "-X",
                "-P", self.password.get(),
                self.input_file.get()
            ]
            
            self.log(f"Running: {' '.join(cmd)}", tab="extract")
            # Same cwd logic for decoder so it can find its 'tables' directory
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
                cwd=os.path.dirname(decode_path)
            )
            
            # MP3Stego decode writes output to '<inputfile>.txt' according to README
            expected_msg_file = f"{self.input_file.get()}.txt"
            if result.returncode == 0 and os.path.exists(expected_msg_file):
                with open(expected_msg_file, "r", encoding="utf-8", errors="ignore") as f:
                    extracted_msg = f.read()
                self.set_message(extracted_msg)
                self.log("Message extracted successfully!", "SUCCESS", "extract")
                messagebox.showinfo("Success", "Message extracted successfully!")
                try:
                    os.remove(expected_msg_file)
                except Exception:
                    pass
            else:
                self.log(f"Error: {result.stderr}", "ERROR", "extract")
                messagebox.showerror("Error", f"Failed to extract message:\n{result.stderr}")
        
        except Exception as e:
            self.log(f"Exception: {str(e)}", "ERROR", "extract")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def find_mp3stego(self):
        """Find MP3Stego executable (Encode.exe for hide, Decode.exe for extract)"""
        # MP3Stego uses Encode.exe for hiding and Decode.exe for extracting
        possible_paths = [
            os.path.join(os.path.dirname(__file__), "..", "Tools", "MP3Stego", "Encode.exe"),
            os.path.join(os.path.dirname(__file__), "..", "tools", "MP3Stego", "Encode.exe"),
            os.path.join(os.path.dirname(__file__), "..", "Tools", "MP3Stego", "Encode.exe"),
            os.path.join(os.path.dirname(__file__), "..", "Tools", "Encode.exe"),
            "Encode.exe",
            "mp3stego.exe",
        ]
        for path in possible_paths:
            abs_path = os.path.abspath(path)
            if os.path.exists(abs_path):
                return abs_path
        return None
    
    def find_mp3stego_decode(self):
        """Find MP3Stego Decode executable"""
        possible_paths = [
            os.path.join(os.path.dirname(__file__), "..", "Tools", "MP3Stego", "Decode.exe"),
            os.path.join(os.path.dirname(__file__), "..", "tools", "MP3Stego", "Decode.exe"),
            os.path.join(os.path.dirname(__file__), "..", "Tools", "Decode.exe"),
            "Decode.exe",
        ]
        for path in possible_paths:
            abs_path = os.path.abspath(path)
            if os.path.exists(abs_path):
                return abs_path
        return None
    
class DeepSoundTool(BaseToolWindow):
    """DeepSound tool implementation"""
    
    def __init__(self, parent, root_window):
        self.root_window = root_window
        super().__init__(parent, "DeepSound")
    
    def create_hide_tab(self, parent):
        """Create Hide tab with audio file types"""
        super().create_hide_tab(parent)
        # Update browse buttons for audio files
        for widget in parent.winfo_children():
            if isinstance(widget, ttk.Button) and widget.cget("text") == "Browse":
                info = widget.grid_info()
                if info.get("row") == 0:
                    widget.config(command=lambda: self.browse_input_file([
                        ("Audio files", "*.wav *.mp3 *.flac"), ("All files", "*.*")
                    ]))
                elif info.get("row") == 1:
                    widget.config(command=lambda: self.browse_output_file([
                        ("Audio files", "*.wav *.mp3 *.flac"), ("All files", "*.*")
                    ]))
    
    def create_extract_tab(self, parent):
        """Create Extract tab with audio file types"""
        super().create_extract_tab(parent)
        # Update browse button for audio files
        for widget in parent.winfo_children():
            if isinstance(widget, ttk.Button) and widget.cget("text") == "Browse":
                widget.config(command=lambda: self.browse_input_file([
                    ("Audio files", "*.wav *.mp3 *.flac"), ("All files", "*.*")
                ]))
    
    def find_deepsound(self):
        """Find DeepSound executable"""
        possible_paths = [
            os.path.join(os.path.dirname(__file__), "..", "Tools", "DeepSound.exe"),
            os.path.join(os.path.dirname(__file__), "..", "tools", "DeepSound.exe"),
            os.path.join(os.path.dirname(__file__), "..", "Tools", "DeepSound", "DeepSound.exe"),
            "DeepSound.exe",
            "deepsound.exe",
        ]
        for path in possible_paths:
            abs_path = os.path.abspath(path)
            if os.path.exists(abs_path):
                return abs_path
        return None
    
    def hide_message(self):
        """Hide message - Launch GUI tool"""
        self.clear_log("hide")
        self.log("Opening DeepSound GUI application...", tab="hide")
        deepsound_path = self.find_deepsound()
        def try_open(path):
            try:
                # If it's a .lnk (shortcut) or any file, use os.startfile on Windows to follow the link.
                if path.lower().endswith('.lnk'):
                    os.startfile(path)
                else:
                    subprocess.Popen([path])
                self.log(f"DeepSound opened successfully: {path}", "SUCCESS", tab="hide")
                messagebox.showinfo("Success", "DeepSound GUI application opened!\nUse the application to hide your message.")
                return True
            except Exception as e:
                self.log(f"Error opening DeepSound: {str(e)}", "ERROR", tab="hide")
                return False

        if deepsound_path and try_open(deepsound_path):
            return

        # If not found or failed to open, prompt the user to locate DeepSound.exe or shortcut
        self.log("DeepSound executable not found or failed to open. Asking user to locate it...", "ERROR", tab="hide")
        user_choice = filedialog.askopenfilename(
            title="Locate DeepSound executable",
            initialdir=os.path.abspath(os.path.join(os.path.dirname(__file__), '..')),
            filetypes=[("Executables", "*.exe;*.lnk"), ("All files", "*.*")]
        )
        if user_choice:
            if try_open(user_choice):
                return
            else:
                messagebox.showerror("Error", f"Failed to open selected file:\n{user_choice}")
        else:
            messagebox.showerror("Error", "DeepSound executable not found.\nPlease ensure DeepSound.exe is available on your system.")
    
    def extract_message(self):
        """Extract message - Launch GUI tool"""
        self.clear_log("extract")
        self.log("Opening DeepSound GUI application...", tab="extract")
        deepsound_path = self.find_deepsound()
        def try_open(path):
            try:
                if path.lower().endswith('.lnk'):
                    os.startfile(path)
                else:
                    subprocess.Popen([path])
                self.log(f"DeepSound opened successfully: {path}", "SUCCESS", tab="extract")
                messagebox.showinfo("Success", "DeepSound GUI application opened!\nUse the application to extract your message.")
                return True
            except Exception as e:
                self.log(f"Error opening DeepSound: {str(e)}", "ERROR", tab="extract")
                return False

        if deepsound_path and try_open(deepsound_path):
            return

        self.log("DeepSound executable not found or failed to open. Asking user to locate it...", "ERROR", tab="extract")
        user_choice = filedialog.askopenfilename(
            title="Locate DeepSound executable",
            initialdir=os.path.abspath(os.path.join(os.path.dirname(__file__), '..')),
            filetypes=[("Executables", "*.exe;*.lnk"), ("All files", "*.*")]
        )
        if user_choice:
            if try_open(user_choice):
                return
            else:
                messagebox.showerror("Error", f"Failed to open selected file:\n{user_choice}")
        else:
            messagebox.showerror("Error", "DeepSound executable not found.\nPlease ensure DeepSound.exe is available on your system.")

