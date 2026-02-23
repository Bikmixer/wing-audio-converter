#!/usr/bin/env python3
"""
Behringer Wing Audio Converter - Cross-Platform Web GUI Server
Provides a beautiful web interface for audio conversion on Windows, Mac, and Linux
"""

import os
import sys
import platform
import wave
import struct
import subprocess
import http.server
import socketserver
import webbrowser
import json
import urllib.parse
import cgi
from pathlib import Path
from typing import List
import threading
import tempfile
import shutil


def get_ffmpeg_path():
    """Get the path to ffmpeg, checking bundled location first."""
    system = platform.system()
    
    # Check if running as PyInstaller bundle
    if getattr(sys, 'frozen', False):
        # Running as bundled app
        base_path = Path(sys._MEIPASS)
        
        # Check multiple possible locations in bundle
        if system == 'Windows':
            ffmpeg_name = 'ffmpeg.exe'
        else:
            ffmpeg_name = 'ffmpeg'
        
        possible_paths = [
            base_path / 'bin' / ffmpeg_name,
            base_path / ffmpeg_name,
            Path(sys.executable).parent / 'bin' / ffmpeg_name,
            Path(sys.executable).parent.parent / 'Frameworks' / 'bin' / ffmpeg_name,
        ]
        
        for ffmpeg_path in possible_paths:
            if ffmpeg_path.exists():
                return str(ffmpeg_path)
    
    # Check system PATH
    try:
        if system == 'Windows':
            result = subprocess.run(['where', 'ffmpeg'], capture_output=True, text=True)
        else:
            result = subprocess.run(['which', 'ffmpeg'], capture_output=True, text=True)
        
        if result.returncode == 0:
            return result.stdout.strip().split('\n')[0]
    except:
        pass
    
    # Common installation paths
    if system == 'Windows':
        common_paths = [
            'C:\\ffmpeg\\bin\\ffmpeg.exe',
            'C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe',
            str(Path.home() / 'ffmpeg' / 'bin' / 'ffmpeg.exe'),
        ]
    elif system == 'Darwin':  # macOS
        common_paths = [
            '/opt/homebrew/bin/ffmpeg',
            '/usr/local/bin/ffmpeg',
            '/usr/bin/ffmpeg',
        ]
    else:  # Linux
        common_paths = [
            '/usr/bin/ffmpeg',
            '/usr/local/bin/ffmpeg',
        ]
    
    for path in common_paths:
        if Path(path).exists():
            return path
    
    return 'ffmpeg.exe' if system == 'Windows' else 'ffmpeg'


class WingAudioConverter:
    def __init__(self, input_file: str, output_dir: str = None, 
                 target_sample_rate: int = None, target_bit_depth: int = None,
                 output_format: str = 'wav'):
        """
        Initialize the audio converter with optional format conversion.
        
        Args:
            input_file: Path to the multi-channel WAV file
            output_dir: Directory to save separated files
            target_sample_rate: Target sample rate (None = keep original)
            target_bit_depth: Target bit depth (None = keep original)
            output_format: Output format ('wav', 'mp3', 'flac', 'aiff')
        """
        self.input_file = Path(input_file)
        
        if not self.input_file.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        if output_dir:
            self.output_dir = Path(output_dir).expanduser()
        else:
            self.output_dir = self.input_file.parent / f"{self.input_file.stem}_separated"
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.target_sample_rate = target_sample_rate
        self.target_bit_depth = target_bit_depth
        self.output_format = output_format.lower()
    
    def convert_with_ffmpeg(self, input_wav: str, output_file: str) -> bool:
        """Convert audio file using ffmpeg if available."""
        try:
            ffmpeg = get_ffmpeg_path()
            cmd = [ffmpeg, '-i', input_wav, '-y']
            
            if self.target_sample_rate:
                cmd.extend(['-ar', str(self.target_sample_rate)])
            
            if self.output_format == 'mp3':
                cmd.extend(['-codec:a', 'libmp3lame', '-q:a', '2'])
            elif self.output_format == 'flac':
                cmd.extend(['-codec:a', 'flac'])
                if self.target_bit_depth:
                    if self.target_bit_depth == 16:
                        cmd.extend(['-sample_fmt', 's16'])
                    elif self.target_bit_depth == 24:
                        cmd.extend(['-sample_fmt', 's32'])
            elif self.output_format == 'aiff':
                if self.target_bit_depth == 16:
                    cmd.extend(['-codec:a', 'pcm_s16be'])
                elif self.target_bit_depth == 24:
                    cmd.extend(['-codec:a', 'pcm_s24be'])
                elif self.target_bit_depth == 32:
                    cmd.extend(['-codec:a', 'pcm_s32be'])
                else:
                    cmd.extend(['-codec:a', 'pcm_s16be'])
            elif self.output_format == 'wav':
                # For WAV with specific bit depth
                if self.target_bit_depth == 16:
                    cmd.extend(['-codec:a', 'pcm_s16le'])
                elif self.target_bit_depth == 24:
                    cmd.extend(['-codec:a', 'pcm_s24le'])
                elif self.target_bit_depth == 32:
                    cmd.extend(['-codec:a', 'pcm_s32le'])
            
            cmd.append(output_file)
            
            subprocess.run(cmd, check=True, capture_output=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def convert(self, channel_names: List[str] = None) -> List[Path]:
        """Convert multi-channel audio to separate files."""
        with wave.open(str(self.input_file), 'rb') as input_wav:
            num_channels = input_wav.getnchannels()
            sample_width = input_wav.getsampwidth()
            frame_rate = input_wav.getframerate()
            num_frames = input_wav.getnframes()
            
            # Create temporary WAV files first
            output_files = []
            temp_wavs = []
            
            for channel in range(num_channels):
                if channel_names and channel < len(channel_names):
                    base_name = channel_names[channel]
                else:
                    base_name = f"channel_{channel + 1:02d}"
                
                # Create temp WAV
                temp_wav = self.output_dir / f"{base_name}_temp.wav"
                temp_wavs.append(temp_wav)
                
                # Determine final output filename
                final_file = self.output_dir / f"{base_name}.{self.output_format}"
                output_files.append(final_file)
            
            # Create output WAV writers
            output_wavs = []
            for temp_wav in temp_wavs:
                wav_out = wave.open(str(temp_wav), 'wb')
                wav_out.setnchannels(1)
                wav_out.setsampwidth(sample_width)
                wav_out.setframerate(frame_rate)
                output_wavs.append(wav_out)
            
            # Process audio in chunks
            chunk_size = 1024
            frames_processed = 0
            
            while frames_processed < num_frames:
                frames_to_read = min(chunk_size, num_frames - frames_processed)
                frames_data = input_wav.readframes(frames_to_read)
                
                # Determine sample format
                if sample_width == 1:
                    format_char = 'B'
                elif sample_width == 2:
                    format_char = 'h'
                elif sample_width == 3:
                    format_char = None
                elif sample_width == 4:
                    format_char = 'i'
                else:
                    raise ValueError(f"Unsupported sample width: {sample_width}")
                
                # Deinterleave channels
                if sample_width == 3:
                    samples = []
                    for i in range(0, len(frames_data), 3 * num_channels):
                        frame = []
                        for ch in range(num_channels):
                            offset = i + ch * 3
                            sample = int.from_bytes(
                                frames_data[offset:offset+3], 
                                byteorder='little', 
                                signed=True
                            )
                            frame.append(sample)
                        samples.append(frame)
                    
                    for ch_idx, wav_out in enumerate(output_wavs):
                        channel_data = b''.join(
                            sample[ch_idx].to_bytes(3, byteorder='little', signed=True)
                            for sample in samples
                        )
                        wav_out.writeframes(channel_data)
                else:
                    samples = struct.unpack(
                        f'<{frames_to_read * num_channels}{format_char}',
                        frames_data
                    )
                    
                    for ch_idx, wav_out in enumerate(output_wavs):
                        channel_samples = samples[ch_idx::num_channels]
                        channel_data = struct.pack(
                            f'<{len(channel_samples)}{format_char}',
                            *channel_samples
                        )
                        wav_out.writeframes(channel_data)
                
                frames_processed += frames_to_read
            
            # Close all temp WAV files
            for wav_out in output_wavs:
                wav_out.close()
        
        # Convert to final format if needed
        needs_conversion = (
            self.output_format != 'wav' or 
            self.target_sample_rate is not None or 
            self.target_bit_depth is not None
        )
        
        if needs_conversion:
            try:
                ffmpeg = get_ffmpeg_path()
                subprocess.run([ffmpeg, '-version'], capture_output=True, check=True)
                has_ffmpeg = True
            except (subprocess.CalledProcessError, FileNotFoundError):
                has_ffmpeg = False
            
            if has_ffmpeg:
                for idx, (temp_wav, final_file) in enumerate(zip(temp_wavs, output_files)):
                    if self.convert_with_ffmpeg(str(temp_wav), str(final_file)):
                        temp_wav.unlink()  # Delete temp file after successful conversion
                    else:
                        # If conversion fails, keep as WAV
                        final_file = temp_wav.parent / f"{temp_wav.stem.replace('_temp', '')}.wav"
                        temp_wav.rename(final_file)
                        output_files[idx] = final_file
            else:
                # No ffmpeg available, keep as WAV
                for idx, temp_wav in enumerate(temp_wavs):
                    final_file = temp_wav.parent / f"{temp_wav.stem.replace('_temp', '')}.wav"
                    temp_wav.rename(final_file)
                    output_files[idx] = final_file
        else:
            # No conversion needed, just rename temp WAV files
            for idx, temp_wav in enumerate(temp_wavs):
                final_file = temp_wav.parent / f"{temp_wav.stem.replace('_temp', '')}.wav"
                temp_wav.rename(final_file)
                output_files[idx] = final_file
        
        return output_files


class WingConverterHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP request handler for the web GUI."""
    
    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/' or self.path == '/index.html':
            # Serve the HTML interface
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html_path = Path(__file__).parent / 'gui_interface.html'
            with open(html_path, 'rb') as f:
                self.wfile.write(f.read())
        elif self.path == '/choose-folder':
            # Open native folder picker (platform-specific)
            try:
                system = platform.system()
                
                if system == 'Darwin':  # macOS
                    result = subprocess.run(
                        ['osascript', '-e', 'POSIX path of (choose folder with prompt "Select Output Folder")'],
                        capture_output=True,
                        text=True,
                        timeout=60
                    )
                elif system == 'Windows':
                    # Use PowerShell folder picker
                    ps_script = '''
                    Add-Type -AssemblyName System.Windows.Forms
                    $browser = New-Object System.Windows.Forms.FolderBrowserDialog
                    $browser.Description = "Select Output Folder"
                    $browser.ShowNewFolderButton = $true
                    if ($browser.ShowDialog() -eq "OK") {
                        Write-Output $browser.SelectedPath
                    }
                    '''
                    result = subprocess.run(
                        ['powershell', '-Command', ps_script],
                        capture_output=True,
                        text=True,
                        timeout=60
                    )
                else:  # Linux
                    # Try zenity or kdialog
                    try:
                        result = subprocess.run(
                            ['zenity', '--file-selection', '--directory', '--title=Select Output Folder'],
                            capture_output=True,
                            text=True,
                            timeout=60
                        )
                    except FileNotFoundError:
                        result = subprocess.run(
                            ['kdialog', '--getexistingdirectory', '.', '--title', 'Select Output Folder'],
                            capture_output=True,
                            text=True,
                            timeout=60
                        )
                
                if result.returncode == 0 and result.stdout.strip():
                    folder_path = result.stdout.strip()
                    response = {'success': True, 'path': folder_path}
                else:
                    response = {'success': False, 'error': 'Folder selection cancelled'}
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
            except Exception as e:
                response = {'success': False, 'error': str(e)}
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
        else:
            super().do_GET()
    
    def do_POST(self):
        """Handle POST requests for file conversion."""
        if self.path == '/convert':
            try:
                print("\n📥 Received conversion request")
                
                # Parse multipart form data
                content_type = self.headers['Content-Type']
                if not content_type.startswith('multipart/form-data'):
                    print("❌ Error: Expected multipart/form-data")
                    self.send_error(400, "Expected multipart/form-data")
                    return
                
                # Get form data
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )
                
                # Get settings
                output_dir = form.getvalue('output_dir', str(Path.home() / 'Desktop'))
                output_format = form.getvalue('output_format', 'wav')
                sample_rate_str = form.getvalue('sample_rate', 'original')
                bit_depth_str = form.getvalue('bit_depth', 'original')
                
                print(f"⚙️  Settings:")
                print(f"   Output Dir: {output_dir}")
                print(f"   Format: {output_format}")
                print(f"   Sample Rate: {sample_rate_str}")
                print(f"   Bit Depth: {bit_depth_str}")
                
                sample_rate = None if sample_rate_str == 'original' else int(sample_rate_str)
                bit_depth = None if bit_depth_str == 'original' else int(bit_depth_str)
                
                # Process uploaded files
                files_processed = 0
                temp_dir = Path(tempfile.mkdtemp())
                print(f"📁 Temp directory: {temp_dir}")
                
                try:
                    if 'files' in form:
                        files = form['files']
                        if not isinstance(files, list):
                            files = [files]
                        
                        print(f"📄 Processing {len(files)} file(s)")
                        
                        for idx, file_item in enumerate(files, 1):
                            filename = getattr(file_item, 'filename', f'file_{idx}')
                            print(f"\n🔄 Converting {idx}/{len(files)}: {filename}")
                            
                            # Save uploaded file temporarily
                            temp_file = temp_dir / filename
                            with open(temp_file, 'wb') as f:
                                file_data = file_item.file.read()
                                f.write(file_data)
                                print(f"   Saved temp file: {len(file_data)} bytes")
                            
                            # Convert the file
                            print(f"   Starting conversion...")
                            converter = WingAudioConverter(
                                str(temp_file),
                                output_dir,
                                target_sample_rate=sample_rate,
                                target_bit_depth=bit_depth,
                                output_format=output_format
                            )
                            output_files = converter.convert()
                            print(f"   ✅ Created {len(output_files)} channel files")
                            files_processed += 1
                    
                    # Send success response
                    output_path = str(Path(output_dir).expanduser().resolve())
                    response = {
                        'success': True,
                        'files_processed': files_processed,
                        'output_dir': output_path
                    }
                    print(f"\n✅ Conversion complete!")
                    print(f"   Files processed: {files_processed}")
                    print(f"   Output directory: {output_path}")
                    
                except Exception as e:
                    print(f"\n❌ Conversion error: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    response = {
                        'success': False,
                        'error': str(e)
                    }
                
                finally:
                    # Clean up temp directory
                    print(f"🧹 Cleaning up temp files...")
                    shutil.rmtree(temp_dir, ignore_errors=True)
                
                # Send JSON response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
                print("📤 Response sent\n")
                
            except Exception as e:
                print(f"\n❌ Server error: {str(e)}")
                import traceback
                traceback.print_exc()
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_response = {'success': False, 'error': str(e)}
                self.wfile.write(json.dumps(error_response).encode())
        else:
            self.send_error(404)
    
    def log_message(self, format, *args):
        """Log important messages only."""
        if 'POST /convert' in format % args or 'GET /' in format % args:
            return  # Suppress these logs as we handle them ourselves
        print(format % args)


def start_server(port=8080):
    """Start the web server and open browser."""
    handler = WingConverterHandler
    
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"🎵 Wing Audio Converter Pro")
        print(f"━" * 50)
        print(f"Server running at: http://localhost:{port}")
        print(f"Opening browser...")
        print(f"Press Ctrl+C to stop the server")
        print(f"━" * 50)
        
        # Open browser
        threading.Timer(1.0, lambda: webbrowser.open(f'http://localhost:{port}')).start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nShutting down server...")


def main():
    """Launch the web GUI."""
    start_server()


if __name__ == '__main__':
    main()
