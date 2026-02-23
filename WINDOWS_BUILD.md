# Building Wing Audio Converter for Windows

Since you don't have a Windows machine, you have two options to create a Windows executable:

## Option 1: GitHub Actions (Recommended - Free Cloud Build)

This uses GitHub's free cloud servers to build the Windows executable automatically.

### Steps:

1. **Create a GitHub repository** (if you don't have one):
   - Go to https://github.com/new
   - Name it: `wing-audio-converter`
   - Make it public or private (your choice)
   - Don't initialize with README

2. **Push your code to GitHub**:
   ```bash
   cd /Users/macstudio/Applications/wing-audio-converter
   
   # Initialize git (if not already done)
   git init
   
   # Add all files
   git add gui_web_crossplatform.py gui_interface.html requirements.txt
   
   # Create .gitignore to exclude build artifacts
   echo "build/
   dist/
   *.spec
   __pycache__/
   *.pyc
   .DS_Store" > .gitignore
   
   git add .gitignore
   
   # Commit
   git commit -m "Initial commit - Wing Audio Converter"
   
   # Add your GitHub repository as remote (replace USERNAME with your GitHub username)
   git remote add origin https://github.com/USERNAME/wing-audio-converter.git
   
   # Push to GitHub
   git push -u origin main
   ```

3. **Create GitHub Actions workflow**:
   - I'll create the workflow file for you (see `.github/workflows/build-windows.yml` below)
   - This will automatically build Windows, macOS, and Linux executables

4. **Download the built executable**:
   - Go to your repository on GitHub
   - Click "Actions" tab
   - Click on the latest workflow run
   - Download the "wing-converter-windows" artifact
   - Unzip it and share the `.exe` file

---

## Option 2: Use Wine on macOS (Build Windows .exe Locally)

Wine allows you to run Windows programs on macOS, including the Windows version of Python.

### Steps:

1. **Install Wine**:
   ```bash
   brew install --cask wine-stable
   ```

2. **Download Windows Python**:
   ```bash
   # Download Python 3.9 for Windows
   curl -o python-3.9.13-amd64.exe https://www.python.org/ftp/python/3.9.13/python-3.9.13-amd64.exe
   
   # Install using Wine
   wine python-3.9.13-amd64.exe /quiet InstallAllUsers=1 PrependPath=1
   ```

3. **Install PyInstaller for Windows**:
   ```bash
   wine python -m pip install pyinstaller
   ```

4. **Download Windows FFmpeg**:
   - Visit: https://www.gyan.dev/ffmpeg/builds/
   - Download "ffmpeg-release-essentials.zip"
   - Extract and place `ffmpeg.exe` in your project folder

5. **Build Windows executable**:
   ```bash
   wine pyinstaller --name "Wing Converter Pro" \
     --windowed \
     --icon=icon.ico \
     --add-data "gui_interface.html;." \
     --add-binary "ffmpeg.exe;bin" \
     gui_web_crossplatform.py
   ```

**Note**: Wine can be unstable and may not work perfectly. GitHub Actions (Option 1) is more reliable.

---

## Option 3: Python Script Version (No Build Required)

Users can run the Python script directly on Windows with minimal setup.

### User Instructions for Windows:

1. **Install Python** (if not installed):
   - Download from https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"

2. **Install FFmpeg**:
   - Download from https://www.gyan.dev/ffmpeg/builds/
   - Extract to `C:\ffmpeg`
   - Add `C:\ffmpeg\bin` to Windows PATH:
     - Search "Environment Variables" in Windows
     - Edit "Path" under System Variables
     - Add new entry: `C:\ffmpeg\bin`

3. **Run the converter**:
   ```cmd
   # Download the files
   # Save gui_web_crossplatform.py and gui_interface.html to a folder
   
   # Run the server
   python gui_web_crossplatform.py
   ```
   
   The browser will open automatically with the converter interface.

---

## Recommended Approach

**For sharing with others**: Use Option 1 (GitHub Actions) to create standalone executables for Windows, macOS, and Linux. Users just download and run - no installation required.

**For personal use**: Option 3 (Python script) works fine if you're comfortable with command line.

**Last resort**: Option 2 (Wine) if you need a local Windows build but it's less reliable.
