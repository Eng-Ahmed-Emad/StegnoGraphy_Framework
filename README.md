# Steganography Toolkit

A comprehensive Python GUI application for various steganography tools, designed for educational and research purposes.

## Features

This toolkit provides a unified interface for multiple steganography tools across different data types:

### Image Steganography
- **Steghide**: Hide and extract messages in images (JPG, PNG, BMP, GIF)
- **Xiao Steganography**: GUI-based image steganography tool

### Audio Steganography
- **MP3Stego**: Hide and extract messages in MP3 audio files
- **DeepSound**: GUI-based audio steganography tool

### Video/GIF Steganography
- **GIF Shuffle Tool**: Hide and extract messages in GIF files
- **Hide it Pro**: GUI-based video steganography tool

### Text Steganography
- **WBStego4Open**: Hide and extract messages in text files (TXT, HTML, XML)
- **S-Tools**: GUI-based steganography tool for images and audio

### ADS Tools (Alternate Data Streams)
- **Streams**: Hide and extract messages using NTFS Alternate Data Streams
- **ADS Viewer**: GUI tool for viewing and managing ADS

### Hex/Binary Steganography
- **Hex Editor Neo**: GUI hex editor for binary file manipulation
- **GMER**: Rootkit detection and binary analysis tool

## Requirements

- Python 3.6 or higher
- tkinter (usually included with Python)
- Windows OS (for some tools like Streams and ADS)

## Installation

1. Clone or download this repository
2. Ensure Python 3.6+ is installed
3. No additional Python packages are required (uses built-in libraries only)

## Usage

### Running the Application

```bash
python steganography_toolkit.py
```

### Using the Tools

1. **Launch the application** - The main window displays all available tool categories
2. **Select a category** - Click on a category button (e.g., "Image Steganography")
3. **Choose a tool** - Select the tool tab you want to use
4. **Configure settings**:
   - Select input file
   - Enter secret message (for hide operations)
   - Enter password if required
   - Specify output file
5. **Execute operation** - Click "Hide Message" or "Extract Message"

### Tool-Specific Notes

#### CLI Tools (Steghide, MP3Stego, etc.)
- These tools require the respective executables to be installed
- If not found, the application will simulate the operation
- Install the tools separately for full functionality

#### GUI Tools (S-Tools, DeepSound, etc.)
- These tools open their standalone GUI applications
- Use the "Open [Tool] GUI" button to launch them
- Follow the tool's own interface for operations

#### ADS Tools
- **Streams**: Works on NTFS file systems only
- Stream names can be specified (default: "hidden")
- Use "List Streams" to view all streams in a file

## Project Structure

```
Stegano project/
├── steganography_toolkit.py    # Main application entry point
├── tools/                       # Tool modules
│   ├── __init__.py
│   ├── base_tool.py            # Base class for all tools
│   ├── image_tools.py          # Image steganography tools
│   ├── audio_tools.py          # Audio steganography tools
│   ├── video_tools.py          # Video/GIF steganography tools
│   ├── text_tools.py           # Text steganography tools
│   ├── ads_tools.py            # ADS tools
│   └── hex_tools.py            # Hex/Binary tools
├── Tools/                       # External tool executables (if available)
│   ├── GIFShuff-Tool/
│   ├── S-Tools/
│   └── SteganographyX Plus/
├── requirements.txt            # Python dependencies (none required)
└── README.md                   # This file
```

## Features

- **Clean GUI Interface**: User-friendly interface built with Tkinter
- **Modular Design**: Each tool is implemented as a separate module
- **Error Handling**: Comprehensive error handling and user feedback
- **Logging**: Built-in log/output area for each tool
- **File Validation**: Input validation for files and required fields
- **Simulation Mode**: Tools can simulate operations when executables are not available

## Limitations

- Some tools require external executables to be installed separately
- GUI-only tools require their standalone applications
- ADS functionality works only on NTFS file systems
- Some operations may require administrator privileges

## Educational Use

This toolkit is designed for educational and research purposes. It demonstrates:
- GUI application development with Python/Tkinter
- Integration of multiple tools in a unified interface
- Steganography techniques across different data types
- Modular software design principles

## Contributing

This is a university project. Contributions and improvements are welcome!

## License

This project is provided for educational purposes.

## Notes

- Always ensure you have permission before hiding data in files
- Some tools may be flagged by antivirus software (false positives)
- Use responsibly and ethically
- For production use, consider implementing actual steganography algorithms rather than simulations

## Troubleshooting

### Tool Not Found Errors
- Ensure the tool executable is installed and accessible
- Check the Tools directory for available executables
- Some tools may need to be added to your system PATH

### ADS Not Working
- Ensure you're using an NTFS file system
- Some operations may require administrator privileges
- Check file permissions

### GUI Tools Not Opening
- Ensure the tool executable exists in the Tools directory
- Check file permissions
- Try running the tool directly to verify it works

## Contact

For questions or issues, please refer to your course instructor or project supervisor.

