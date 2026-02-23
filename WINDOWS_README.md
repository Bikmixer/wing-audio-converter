# Wing Audio Converter Pro - Windows Instructions

## Quick Start (Python Script Version)

### Prerequisites

1. **Install Python 3.9 or later**
   - Download from https://www.python.org/downloads/
   - **IMPORTANT**: During installation, check "Add Python to PATH"

2. **Install FFmpeg**
   
   **Option A - Using Chocolatey (Easiest)**:
   ```cmd
   # Open PowerShell as Administrator and run:
   Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   
   # Then install ffmpeg:
   choco install ffmpeg
   ```
   
   **Option B - Manual Installation**:
   - Download from https://www.gyan.dev/ffmpeg/builds/
   - Click "ffmpeg-release-essentials.zip"
   - Extract the ZIP file to `C:\ffmpeg`
   - Add to PATH:
     1. Press `Win + X` and select "System"
     2. Click "Advanced system settings"
     3. Click "Environment Variables"
     4. Under "System variables", find "Path" and click "Edit"
     5. Click "New" and add: `C:\ffmpeg\bin`
     6. Click "OK" to close all dialogs
     7. Restart your computer

### Running the Converter

1. **Download the files**:
   - Download `gui_web_crossplatform.py` and `gui_interface.html`
   - Put them in the same folder (e.g., `C:\WingConverter`)

2. **Open Command Prompt**:
   - Press `Win + R`
   - Type `cmd` and press Enter
   - Navigate to your folder:
     ```cmd
     cd C:\WingConverter
     ```

3. **Run the converter**:
   ```cmd
   python gui_web_crossplatform.py
   ```
   
   Your browser will automatically open with the converter interface.

### Using the Converter

1. **Add Files**:
   - Drag and drop WAV files onto the left panel
   - Or click "Choose Files" to browse

2. **Select Output Location**:
   - Click "Browse Folder" (will open Windows folder picker)
   - Or type the path manually

3. **Choose Settings**:
   - **Format**: WAV, MP3, FLAC, or AIFF
   - **Sample Rate**: Keep original or convert to 44.1kHz, 48kHz, or 96kHz
   - **Bit Depth**: Keep original or convert to 16-bit, 24-bit, or 32-bit

4. **Convert**:
   - Click "Start Conversion"
   - Wait for completion
   - Find your files in the output folder

### Troubleshooting

**"Python is not recognized"**:
- Reinstall Python and make sure to check "Add Python to PATH"
- Or add Python to PATH manually (similar to FFmpeg steps above)

**"ffmpeg is not recognized"**:
- Make sure FFmpeg is installed and added to PATH
- Restart your computer after adding to PATH
- Test by opening new Command Prompt and typing: `ffmpeg -version`

**Browser doesn't open automatically**:
- Manually open your browser and go to: http://localhost:8080

**"Address already in use" error**:
- Another program is using port 8080
- Close the other program or restart your computer

### Creating Desktop Shortcut

1. Create a new file named `Wing Converter.bat` with this content:
   ```batch
   @echo off
   cd C:\WingConverter
   python gui_web_crossplatform.py
   pause
   ```

2. Right-click the `.bat` file → "Create shortcut"

3. Move the shortcut to your Desktop

4. Double-click the shortcut to launch the converter

---

## Standalone Executable Version (No Python Installation Required)

If you prefer a double-click executable that doesn't require Python installation:

1. **Download the pre-built executable**:
   - Go to the GitHub releases page
   - Download `Wing-Converter-Pro-Windows.zip`
   - Extract the ZIP file

2. **Run the app**:
   - Double-click `Wing Converter Pro.exe`
   - Your browser will open with the converter

**Note**: The standalone version is larger (100+ MB) because it includes Python and FFmpeg bundled inside.

---

## System Requirements

- **OS**: Windows 10 or later (64-bit)
- **RAM**: 4GB minimum, 8GB recommended
- **Disk Space**: 500MB free space for installation and temporary files
- **Browser**: Any modern browser (Chrome, Firefox, Edge)

---

## Support

For issues or questions, check the main README or create an issue on GitHub.
