from faster_whisper import WhisperModel
import json
import os
import time

class TranscriptionService:
    def __init__(self, model_size="medium"):
        """Initialize transcription service"""
        self.input_dir = "input"
        self.output_dir = "output"
        
        # Create directories if they don't exist
        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        
        print(f"Loading Whisper {model_size} model...")
        self.model = WhisperModel(model_size, device="cuda" if self.has_gpu() else "cpu")
        print("Model loaded!")

    def has_gpu(self):
        """Check if GPU is available"""
        try:
            import torch
            return torch.cuda.is_available()
        except ImportError:
            return False

    def transcribe(self, audio_path, source_language=None):
        """Transcribe audio file with word-level timestamps"""
        try:
            if not os.path.exists(audio_path):
                raise FileNotFoundError(f"Audio file not found: {audio_path}")

            print(f"Transcribing {audio_path}...")
            segments, info = self.model.transcribe(
                audio_path,
                language=source_language,
                word_timestamps=True
            )

            result = {
                "language": source_language or info.language,
                "segments": []
            }

            for segment in segments:
                words = [{
                    "word": word.word,
                    "start": word.start,
                    "end": word.end,
                    "confidence": word.probability
                } for word in segment.words]

                result["segments"].append({
                    "text": segment.text,
                    "start": segment.start,
                    "end": segment.end,
                    "words": words
                })

            return result

        except Exception as e:
            print(f"Error during transcription: {str(e)}")
            raise

    def save_formatted_transcript(self, result, audio_file):
        """Save transcript in a format ready for translation"""
        try:
            duration = result["segments"][-1]["end"] if result["segments"] else 0
            base_name = os.path.splitext(os.path.basename(audio_file))[0]
            
            # Create output directory for this file
            file_output_dir = os.path.join(self.output_dir, base_name)
            os.makedirs(file_output_dir, exist_ok=True)
            
            json_path = os.path.join(file_output_dir, f"{base_name}_transcript.json")
            
            total_words = sum(len(segment["words"]) for segment in result["segments"])
            total_confidence = sum(word["confidence"] for segment in result["segments"] 
                                 for word in segment["words"])
            
            formatted = {
                "metadata": {
                    "language": result["language"],
                    "duration": duration,
                    "word_count": total_words,
                    "segment_count": len(result["segments"]),
                    "average_confidence": total_confidence / total_words if total_words > 0 else 0,
                    "original_file": audio_file
                },
                "segments": [
                    {
                        "id": i,
                        "text": segment["text"],
                        "start": segment["start"],
                        "end": segment["end"],
                        "confidence": sum(w["confidence"] for w in segment["words"]) / len(segment["words"]),
                        "words": segment["words"]
                    }
                    for i, segment in enumerate(result["segments"])
                ]
            }
            
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(formatted, f, indent=2, ensure_ascii=False)
                
            print(f"Formatted transcript saved to: {json_path}")
            return formatted
            
        except Exception as e:
            print(f"Error saving formatted transcript: {str(e)}")
            raise

    def process_file(self, audio_file, language=None):
        """Process a single audio file"""
        try:
            result = self.transcribe(audio_file, language)
            formatted = self.save_formatted_transcript(result, audio_file)
            
            # Print summary
            print("\nTranscription Summary:")
            print(f"Language: {formatted['metadata']['language']}")
            print(f"Duration: {formatted['metadata']['duration']:.2f} seconds")
            print(f"Word Count: {formatted['metadata']['word_count']}")
            print(f"Segments: {formatted['metadata']['segment_count']}")
            print(f"Average Confidence: {formatted['metadata']['average_confidence']:.2%}")
            
            return True
        except Exception as e:
            print(f"Error processing {audio_file}: {str(e)}")
            return False

    def watch_input_directory(self):
        """Watch input directory for new files"""
        print(f"Watching input directory: {self.input_dir}")
        print("Waiting for audio files... (Press Ctrl+C to exit)")
        
        while True:
            try:
                # Check input directory for files
                files_processed = False
                for file in os.listdir(self.input_dir):
                    if file.endswith(('.wav', '.mp3')):
                        input_path = os.path.join(self.input_dir, file)
                        print(f"\nFound new file: {file}")
                        
                        if self.process_file(input_path):
                            # Move or delete processed file
                            os.remove(input_path)
                            print(f"Processed and removed: {file}")
                            files_processed = True
                
                if files_processed:
                    print("\nAll files processed. Press Ctrl+C to exit or wait for new files...")
                
                time.sleep(5)  # Check every 5 seconds
                
            except KeyboardInterrupt:
                print("\nExiting service...")
                break
            except Exception as e:
                print(f"Error in watch loop: {str(e)}")
                time.sleep(5)  # Wait before retrying

if __name__ == "__main__":
    service = TranscriptionService(model_size="base")
    service.watch_input_directory()