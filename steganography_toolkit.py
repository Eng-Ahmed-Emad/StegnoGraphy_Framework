"""
Steganography Toolkit - Main Application
A comprehensive GUI application for various steganography tools
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys

# Add current directory to path to ensure imports work
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Handle Windows case-sensitivity: ensure tools module can be imported
# On Windows, "Tools" and "tools" are the same directory, but Python imports are case-sensitive
tools_dir = None
for name in ["tools", "Tools"]:
    test_path = os.path.join(current_dir, name)
    if os.path.exists(test_path) and os.path.isdir(test_path):
        tools_dir = test_path
        # Add the parent directory to path so we can import 'tools'
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        break

# Import tool modules
try:
    from tools.image_tools import ImageStegoWindow
    from tools.audio_tools import AudioStegoWindow
    from tools.video_tools import VideoStegoWindow
    from tools.text_tools import TextStegoWindow
    from tools.ads_tools import ADSToolsWindow
    from tools.hex_tools import HexStegoWindow
except ImportError:
    # Fallback: try importing with different case or direct path
    import importlib.util
    import importlib
    
    # Create tools module namespace
    if "tools" not in sys.modules:
        import types
        tools_pkg = types.ModuleType("tools")
        sys.modules["tools"] = tools_pkg
    
    # Import each module
    for mod_name, class_name in [
        ("image_tools", "ImageStegoWindow"),
        ("audio_tools", "AudioStegoWindow"),
        ("video_tools", "VideoStegoWindow"),
        ("text_tools", "TextStegoWindow"),
        ("ads_tools", "ADSToolsWindow"),
        ("hex_tools", "HexStegoWindow"),
    ]:
        mod_path = os.path.join(tools_dir or os.path.join(current_dir, "tools"), f"{mod_name}.py")
        if os.path.exists(mod_path):
            spec = importlib.util.spec_from_file_location(f"tools.{mod_name}", mod_path)
            if spec and spec.loader:
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                sys.modules[f"tools.{mod_name}"] = mod
                globals()[class_name] = getattr(mod, class_name)


class SteganographyToolkit:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography Toolkit")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="Steganography Toolkit",
            font=("Arial", 24, "bold")
        )
        title_label.grid(row=0, column=0, pady=(0, 30))
        
        # Subtitle
        subtitle_label = ttk.Label(
            main_frame,
            text="Select a category to access steganography tools",
            font=("Arial", 12)
        )
        subtitle_label.grid(row=1, column=0, pady=(0, 30))
        
        # Category buttons frame
        categories_frame = ttk.Frame(main_frame)
        categories_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        categories_frame.columnconfigure(0, weight=1)
        categories_frame.columnconfigure(1, weight=1)
        
        # Image Stego
        self.create_category_button(
            categories_frame, 0, 0,
            "Image Steganography",
            "Steghide\nXiao Steganography",
            lambda: ImageStegoWindow(self.root)
        )
        
        # Audio Stego
        self.create_category_button(
            categories_frame, 0, 1,
            "Audio Steganography",
            "MP3Stego\nDeepSound",
            lambda: AudioStegoWindow(self.root)
        )
        
        # Video/GIF Stego
        self.create_category_button(
            categories_frame, 1, 0,
            "Video/GIF Steganography",
            "GIF Shuffle Tool",
            lambda: VideoStegoWindow(self.root)
        )
        
        # Text Stego
        self.create_category_button(
            categories_frame, 1, 1,
            "Text Steganography",
            "WBStego4Open\nS-Tools",
            lambda: TextStegoWindow(self.root)
        )
        
        # ADS Tools
        self.create_category_button(
            categories_frame, 2, 0,
            "ADS Tools",
            "Streams\nADS Viewer",
            lambda: ADSToolsWindow(self.root)
        )
        
        # Hex/Binary Stego
        self.create_category_button(
            categories_frame, 2, 1,
            "Hex/Binary Steganography",
            "Hex Editor Neo\nGMER",
            lambda: HexStegoWindow(self.root)
        )
        
        # Footer
        footer_label = ttk.Label(
            main_frame,
            text="University Project - Steganography Toolkit",
            font=("Arial", 9),
            foreground="gray"
        )
        footer_label.grid(row=3, column=0, pady=(30, 0))
    
    def create_category_button(self, parent, row, col, title, tools, command):
        """Create a styled category button"""
        button_frame = ttk.Frame(parent, relief="raised", borderwidth=2)
        button_frame.grid(row=row, column=col, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        button_frame.columnconfigure(0, weight=1)
        
        title_label = ttk.Label(
            button_frame,
            text=title,
            font=("Arial", 14, "bold")
        )
        title_label.grid(row=0, column=0, pady=(15, 5))
        
        tools_label = ttk.Label(
            button_frame,
            text=tools,
            font=("Arial", 10),
            foreground="darkblue"
        )
        tools_label.grid(row=1, column=0, pady=(0, 10))
        
        open_button = ttk.Button(
            button_frame,
            text="Open Tools",
            command=command
        )
        open_button.grid(row=2, column=0, pady=(0, 15))


def main():
    root = tk.Tk()
    app = SteganographyToolkit(root)
    root.mainloop()


if __name__ == "__main__":
    main()

