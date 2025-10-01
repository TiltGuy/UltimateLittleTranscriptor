# AudioTranscriptor

A simple Python application for recording audio and transcribing it using OpenAI's Whisper model.

## Features

- **Keyboard-controlled recording**: Press 'T' to start recording, 'P' to stop
- **Automatic transcription**: Transcribes all audio files in the Recordings directory
- **Multiple language support**: Configure transcription language via command-line arguments
- **Live progress indicators**: Real-time feedback during recording and transcription
- **Batch processing**: Transcribes multiple audio files automatically

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py --language "fr" --model_size "base"
```

## Usage

### Command-line Arguments

- `--model_size`: Whisper model size (default: "base"). Options: tiny, base, small, medium, large
- `--language`: Audio language for transcription (default: "en"). Example: "fr" for French
- `--output_dir`: Directory to save transcriptions (default: "./Transcriptions")
- `--verbose`: Show detailed transcription output (default: False)

### Controls

- Press **T**: Start recording audio
- Press **P**: Stop recording
- Press **X**: Exit the application

### How It Works

1. **Recording**: Audio is recorded at 44.1kHz mono and saved to `./Recordings/` with timestamp-based filenames
2. **Transcription**: After recording stops, all audio files in the Recordings directory are transcribed using Whisper
3. **Output**: Transcriptions are saved as `.txt` files in the output directory (default: `./Transcriptions/`)

## File Structure

- `app.py`: Main application file
- `requirements.txt`: Python dependencies
- `Recordings/`: Directory for recorded audio files (created automatically)
- `Transcriptions/`: Directory for transcription output (created automatically)

## Supported Audio Formats

- `.wav`
- `.mp3`
- `.m4a`
