# Behringer Wing Audio Converter

A Python tool to convert multi-channel audio recordings from the Behringer Wing digital mixer to separate audio files.

## Features

- Converts multi-track WAV files to individual mono files
- Supports 8, 16, 24, and 32-bit audio
- Custom channel naming
- Progress indicator
- Efficient chunk-based processing

## Requirements

- Python 3.6 or higher
- No external dependencies (uses built-in `wave` module)

## Installation

Simply download `audio_converter.py` - no installation needed!

## Usage

### Basic Usage

Convert a multi-channel WAV file to separate files:

```bash
python audio_converter.py recording.wav
```

This will create a directory called `recording_separated/` with files named `channel_01.wav`, `channel_02.wav`, etc.

### Custom Output Directory

Specify where to save the separated files:

```bash
python audio_converter.py recording.wav -o /path/to/output
```

### Named Channels

Provide custom names for each channel:

```bash
python audio_converter.py recording.wav -n "Kick,Snare,HiHat,Overhead_L,Overhead_R,Bass,Guitar,Vocals"
```

This will create files named `Kick.wav`, `Snare.wav`, etc.

### Complete Example

```bash
python audio_converter.py live_show.wav \
  -o processed_tracks \
  -n "Kick,Snare,Tom1,Tom2,HiHat,OH_L,OH_R,Bass_DI,Guitar_L,Guitar_R,Vocals_Lead,Vocals_BG1,Vocals_BG2"
```

## Behringer Wing Recording Format

The Behringer Wing records multi-track audio to SD cards in WAV format:
- Typically 48kHz sample rate
- 24-bit or 32-bit depth
- All channels interleaved in a single file
- Up to 48 channels can be recorded

## Output

Each channel is saved as a separate mono WAV file with:
- Same sample rate as input
- Same bit depth as input
- Sequential numbering or custom names

## Troubleshooting

**File not found error**: Make sure the path to your WAV file is correct.

**Memory issues with large files**: The converter processes audio in chunks, so it should handle files of any size.

**Unsupported format**: Ensure your file is a standard WAV format. The Wing outputs standard WAV files which should work with this tool.

## License

Free to use and modify.
