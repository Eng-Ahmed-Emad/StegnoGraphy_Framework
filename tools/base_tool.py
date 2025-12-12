"""
Base Tool Window Class
Provides common functionality for all tool windows
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os


class BaseToolWindow:
    """Base class for all tool windows"""
    
    def __init__(self, parent, tool_name):
        self.parent = parent
        self.tool_name = tool_name
        self.window = parent  # Use parent frame directly
        
        # Variables
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        self.message = tk.StringVar()
        self.password = tk.StringVar()
        
        self.create_tabbed_widgets()
    
    def create_tabbed_widgets(self):
        """Create tabbed interface with Hide and Extract tabs"""
        # Create notebook for Hide/Extract tabs
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Hide tab
        hide_frame = ttk.Frame(notebook, padding="15")
        notebook.add(hide_frame, text="Hide Message")
        self.create_hide_tab(hide_frame)
        
        # Extract tab
        extract_frame = ttk.Frame(notebook, padding="15")
        notebook.add(extract_frame, text="Extract Message")
        self.create_extract_tab(extract_frame)
    
    def create_hide_tab(self, parent):
        """Create the Hide Message tab - override in subclasses"""
        parent.columnconfigure(1, weight=1)
        
        # Input file
        ttk.Label(parent, text="Input File:", font=("Arial", 10)).grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        ttk.Entry(parent, textvariable=self.input_file, width=50).grid(
            row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5
        )
        ttk.Button(parent, text="Browse", command=self.browse_input_file).grid(
            row=0, column=2, padx=5, pady=5
        )
        
        # Output file
        ttk.Label(parent, text="Output File:", font=("Arial", 10)).grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        ttk.Entry(parent, textvariable=self.output_file, width=50).grid(
            row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5
        )
        ttk.Button(parent, text="Browse", command=self.browse_output_file).grid(
            row=1, column=2, padx=5, pady=5
        )
        
        # Message input
        ttk.Label(parent, text="Secret Message:", font=("Arial", 10)).grid(
            row=2, column=0, sticky=tk.NW, pady=5
        )
        self.message_text = scrolledtext.ScrolledText(
            parent,
            width=50,            height=8,
            wrap=tk.WORD
        )
        self.message_text.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        # Password input (optional, can be overridden)
        ttk.Label(parent, text="Password:", font=("Arial", 10)).grid(
            row=3, column=0, sticky=tk.W, pady=5
        )
        password_entry = ttk.Entry(parent, textvariable=self.password, width=50, show="*")
        password_entry.grid(row=3, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Hide button
        hide_button = ttk.Button(
            parent,
            text="Hide Message",
            command=self.hide_message,
            width=25
        )
        hide_button.grid(row=4, column=0, columnspan=3, pady=20)
        
        # Log area
        ttk.Label(parent, text="Output/Log:", font=("Arial", 10)).grid(
            row=5, column=0, sticky=tk.NW, pady=(10, 5)
        )
        self.hide_log_text = scrolledtext.ScrolledText(
            parent,
            width=70,
            height=8,
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.hide_log_text.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        parent.rowconfigure(6, weight=1)
        parent.rowconfigure(2, weight=1)
    
    def create_extract_tab(self, parent):
        """Create the Extract Message tab - override in subclasses"""
        parent.columnconfigure(1, weight=1)
        
        # Input file
        ttk.Label(parent, text="Input File:", font=("Arial", 10)).grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        ttk.Entry(parent, textvariable=self.input_file, width=50).grid(
            row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5
        )
        ttk.Button(parent, text="Browse", command=self.browse_input_file).grid(
            row=0, column=2, padx=5, pady=5
        )
        
        # Password input (optional, can be overridden)
        ttk.Label(parent, text="Password:", font=("Arial", 10)).grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        password_entry = ttk.Entry(parent, textvariable=self.password, width=50, show="*")
        password_entry.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Extract button
        extract_button = ttk.Button(
            parent,
            text="Extract Message",
            command=self.extract_message,
            width=25
        )
        extract_button.grid(row=2, column=0, columnspan=3, pady=20)
        
        # Extracted message display
        ttk.Label(parent, text="Extracted Message:", font=("Arial", 10)).grid(
            row=3, column=0, sticky=tk.NW, pady=(10, 5)
        )
        self.extracted_message_text = scrolledtext.ScrolledText(
            parent,
            width=70,
            height=10,
            wrap=tk.WORD,
            state=tk.NORMAL
        )
        self.extracted_message_text.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        # Log area
        ttk.Label(parent, text="Output/Log:", font=("Arial", 10)).grid(
            row=5, column=0, sticky=tk.NW, pady=(10, 5)
        )
        self.extract_log_text = scrolledtext.ScrolledText(
            parent,
            width=70,
            height=6,
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.extract_log_text.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        parent.rowconfigure(4, weight=1)
        parent.rowconfigure(6, weight=1)
    
    def browse_input_file(self, filetypes=None):
        """Browse for input file"""
        if filetypes is None:
            filetypes = [("All files", "*.*")]
        
        filename = filedialog.askopenfilename(
            title="Select Input File",
            filetypes=filetypes
        )
        if filename:
            self.input_file.set(filename)
            # Auto-set output file if not set
            if not self.output_file.get():
                base, ext = os.path.splitext(filename)
                self.output_file.set(f"{base}_stego{ext}")
    
    def browse_output_file(self, filetypes=None):
        """Browse for output file"""
        if filetypes is None:
            filetypes = [("All files", "*.*")]
        
        filename = filedialog.asksaveasfilename(
            title="Save Output File",
            filetypes=filetypes,
            defaultextension=""
        )
        if filename:
            self.output_file.set(filename)
    
    def get_message(self):
        """Get message from text widget"""
        return self.message_text.get("1.0", tk.END).strip()
    
    def set_message(self, text):
        """Set message in extracted message text widget"""
        try:
            if hasattr(self, 'extracted_message_text'):
                if self.extracted_message_text.winfo_exists():
                    self.extracted_message_text.config(state=tk.NORMAL)
                    self.extracted_message_text.delete("1.0", tk.END)
                    self.extracted_message_text.insert("1.0", text)
                    self.extracted_message_text.config(state=tk.NORMAL)
                else:
                    # Widget doesn't exist - this shouldn't happen in normal operation
                    pass
            else:
                # Attribute doesn't exist - this shouldn't happen in normal operation
                pass
        except Exception as e:
            # Log error for debugging but don't crash
            pass
    
    def log(self, message, level="INFO", tab="hide"):
        """Add message to log area"""
        if tab == "hide":
            log_widget = self.hide_log_text
        else:
            log_widget = self.extract_log_text
        
        log_widget.config(state=tk.NORMAL)
        log_widget.insert(tk.END, f"[{level}] {message}\n")
        log_widget.see(tk.END)
        log_widget.config(state=tk.DISABLED)
    
    def clear_log(self, tab="hide"):
        """Clear the log area"""
        if tab == "hide":
            log_widget = self.hide_log_text
        else:
            log_widget = self.extract_log_text
        
        log_widget.config(state=tk.NORMAL)
        log_widget.delete("1.0", tk.END)
        log_widget.config(state=tk.DISABLED)
    
    def hide_message(self):
        """Hide message - override in subclasses"""
        self.log("Hide message functionality not implemented", "ERROR", "hide")
        messagebox.showwarning("Not Implemented", "Hide message functionality not implemented for this tool.")
    
    def extract_message(self):
        """Extract message - override in subclasses"""
        self.log("Extract message functionality not implemented", "ERROR", "extract")
        messagebox.showwarning("Not Implemented", "Extract message functionality not implemented for this tool.")
    
    def validate_inputs(self, require_message=True, require_password=False, tab="hide"):
        """Validate input fields"""
        if not self.input_file.get():
            messagebox.showerror("Error", "Please select an input file.")
            return False
        
        if not os.path.exists(self.input_file.get()):
            messagebox.showerror("Error", "Input file does not exist.")
            return False
        
        if require_message and not self.get_message():
            messagebox.showerror("Error", "Please enter a secret message.")
            return False
        
        if require_password and not self.password.get():
            messagebox.showerror("Error", "Password is required for this tool.")
            return False
        
        return True


def find_executable(possible_paths):
    """Return the first existing absolute path from the list or None.
    Accepts a list of relative or absolute paths and returns the absolute path
    of the first file that exists.
    """
    for path in possible_paths:
        abs_path = os.path.abspath(path)
        if os.path.exists(abs_path):
            return abs_path
    return None


def launch_executable(path, follow_lnk=True, cwd=None, extra_args=None):
    """Launch an executable or shortcut.
    - If `path` ends with `.lnk` and `follow_lnk` is True, use `os.startfile` to follow the shortcut on Windows.
    - Otherwise, use `subprocess.Popen` with `cwd` defaulting to the executable directory.
    - `extra_args` may be a list of additional command-line arguments to pass after the executable path.
    Returns True if launch started, False otherwise.
    """
    import subprocess
    try:
        if follow_lnk and path.lower().endswith('.lnk'):
            # os.startfile will follow the shortcut and ignore extra args
            os.startfile(path)
            return True
        abs_path = os.path.abspath(path)
        run_cwd = cwd or os.path.dirname(abs_path)
        cmd = [abs_path]
        if extra_args:
            cmd += list(extra_args)
        subprocess.Popen(cmd, cwd=run_cwd)
        return True
    except Exception:
        return False
