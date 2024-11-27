import os
import json
import time
import elevenlabs

class DubbingService:
    def __init__(self, api_key):
        """Initialize dubbing service"""
        print("Initializing Dubbing Service...")
        elevenlabs.api_key = api_key
        self.input_dir = "input"
        self.output_dir = "output"
        
        # Create directories
        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        print("Service initialized!")

    def generate_speech_segment(self, text):
        """Generate speech for a segment"""
        try:
            print(f"Generating speech for text: {text[:50]}...")
            audio = elevenlabs.generate(
                text=text,
                voice="Rachel",
                model="eleven_multilingual_v2"
            )
            return audio
        except Exception as e:
            print(f"Error generating speech: {str(e)}")
            raise

    def process_translation(self, input_file):
        """Process a single translation file"""
        try:
            print(f"Processing file: {input_file}")
            # Read input JSON
            with open(input_file, 'r', encoding='utf-8') as f:
                translation = json.load(f)

            base_name = os.path.splitext(os.path.basename(input_file))[0]
            output_dir = os.path.join(self.output_dir, base_name)
            os.makedirs(output_dir, exist_ok=True)

            # Generate speech for each segment
            for segment in translation["segments"]:
                print(f"Generating speech for segment {segment['id']}...")
                
                audio = self.generate_speech_segment(segment["translated_text"])
                
                # Save segment audio
                segment_file = os.path.join(output_dir, f"segment_{segment['id']}.mp3")
                with open(segment_file, "wb") as f:
                    f.write(audio)
                print(f"Saved segment {segment['id']}")

            print(f"All segments generated in: {output_dir}")
            return True

        except Exception as e:
            print(f"Error processing {input_file}: {str(e)}")
            return False

    def watch_input_directory(self):
        """Watch input directory for new translation files"""
        print(f"Watching input directory: {self.input_dir}")
        print("Waiting for translation files... (Press Ctrl+C to exit)")
        
        while True:
            try:
                files = os.listdir(self.input_dir)
                print(f"\nChecking directory... Found {len(files)} files")
                
                for file in files:
                    if file.endswith('_translation.json'):
                        input_path = os.path.join(self.input_dir, file)
                        print(f"\nFound new translation: {file}")
                        
                        if self.process_translation(input_path):
                            # Move or delete processed file
                            os.remove(input_path)
                            print(f"Processed and removed: {file}")
                    else:
                        print(f"Skipping non-translation file: {file}")
                
                time.sleep(5)  # Check every 5 seconds
                
            except KeyboardInterrupt:
                print("\nExiting service...")
                break
            except Exception as e:
                print(f"Error in watch loop: {str(e)}")
                time.sleep(5)

if __name__ == "__main__":
    api_key = "sk_a7c92e88c2dd78a2fdea3386971adf3df6c60d541d0bad97"
    print("Starting Dubbing Service...")
    service = DubbingService(api_key)
    service.watch_input_directory()
