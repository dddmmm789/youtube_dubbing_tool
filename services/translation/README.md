
# Transcription Service

## Overview
This project provides an audio transcription service that processes input audio files to generate a detailed transcript. The service includes segmentation, word-level timestamps, and confidence levels for each segment and word. It leverages AI models for efficient and accurate transcription.

## Features
- **High-Accuracy Transcription**: Supports English audio with confidence levels for each word and segment.
- **Segmented Output**: Provides timestamps and segmentation for easy analysis.
- **JSON Output**: Saves the transcription in a structured JSON format for integration with other applications.
- **Lightweight Dependencies**: Optimized for performance with minimal external libraries.

## Files in the Project
1. **transcription_service.py**: Main Python script implementing the transcription service.
2. **vocals_transcript.json**: Sample output file demonstrating the transcription capabilities.
3. **requirements.txt**: Contains the dependencies required to run the project.

## Dependencies
The following Python packages are required:
- `faster-whisper`: For transcription.
- `numpy`: For numerical computations.

## Installation
1. Clone this repository:
   ```bash
   git clone [repository_url]
   cd [repository_folder]
   ```
2. Create a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Place your input audio file (e.g., `vocals.wav`) in the `input` directory.
2. Run the transcription service:
   ```bash
   python transcription_service.py
   ```
3. The transcribed output will be saved as a JSON file in the project directory (e.g., `vocals_transcript.json`).

## Output Format
The transcription output is saved in a JSON format with the following structure:
- **metadata**:
  - `language`: Language of the audio.
  - `duration`: Duration of the audio in seconds.
  - `word_count`: Total number of words in the transcription.
  - `segment_count`: Total number of segments.
  - `average_confidence`: Average confidence score across all words.
  - `original_file`: Path to the original audio file.
- **segments**: A list of transcribed segments with:
  - `id`: Segment ID.
  - `text`: Full text of the segment.
  - `start` and `end`: Start and end timestamps of the segment.
  - `confidence`: Confidence score for the segment.
  - `words`: Detailed breakdown of words with individual timestamps and confidence scores.

## Example Output
```json
{
  "metadata": {
    "language": "en",
    "duration": 60.16,
    "word_count": 215,
    "segment_count": 13,
    "average_confidence": 0.9221,
    "original_file": "input/vocals.wav"
  },
  "segments": [
    {
      "id": 0,
      "text": "Amazon sucks right now, Uber sucks right now...",
      "start": 0.0,
      "end": 4.74,
      "confidence": 0.9585,
      "words": [
        {"word": "Amazon", "start": 0.0, "end": 0.42, "confidence": 0.9203},
        ...
      ]
    }
  ]
}
```

## Future Improvements
- Add support for multiple languages.
- Implement real-time transcription for streaming audio.
- Enhance UI for easier interaction.

## License
[Specify the license if applicable.]
