# services/translation/translation_service.py
import os
import json
import time
import deepl

class TranslationService:
    def __init__(self, auth_key):
        """Initialize translation service"""
        try:
            self.translator = deepl.Translator(auth_key)
            print("DeepL API connected successfully!")
            print(f"Character usage: {self.translator.get_usage().character.count}/{self.translator.get_usage().character.limit}")
            
            self.input_dir = "input"
            self.output_dir = "output"
            
            # Create directories if they don't exist
            os.makedirs(self.input_dir, exist_ok=True)
            os.makedirs(self.output_dir, exist_ok=True)
        except Exception as e:
            print(f"Error initializing DeepL: {str(e)}")
            raise

    def translate_text(self, text, target_lang):
        """Translate text while preserving formatting"""
        try:
            result = self.translator.translate_text(text, target_lang=target_lang)
            return result.text
        except Exception as e:
            print(f"Translation error: {str(e)}")
            raise

    def process_transcript(self, input_file, target_lang):
        """Process a single transcript file"""
        try:
            # Read input JSON
            with open(input_file, 'r', encoding='utf-8') as f:
                transcript = json.load(f)

            # Create output structure
            base_name = os.path.splitext(os.path.basename(input_file))[0]
            output = {
                "metadata": {
                    "source_language": transcript["metadata"]["language"],
                    "target_language": target_lang,
                    "duration": transcript["metadata"]["duration"],
                    "word_count": transcript["metadata"]["word_count"],
                    "segment_count": transcript["metadata"]["segment_count"],
                    "original_file": transcript["metadata"]["original_file"],
                    "source_transcript": input_file
                },
                "segments": []
            }

            # Translate each segment
            for segment in transcript["segments"]:
                translated_text = self.translate_text(segment["text"], target_lang)
                
                output["segments"].append({
                    "id": segment["id"],
                    "source_text": segment["text"],
                    "translated_text": translated_text,
                    "start": segment["start"],
                    "end": segment["end"],
                    "words": segment["words"]  # Keeping original timing
                })

            # Save translated output
            output_dir = os.path.join(self.output_dir, base_name)
            os.makedirs(output_dir, exist_ok=True)
            
            output_file = os.path.join(output_dir, f"{base_name}_{target_lang}_translation.json")
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=2, ensure_ascii=False)

            print(f"Translation saved to: {output_file}")
            return True

        except Exception as e:
            print(f"Error processing {input_file}: {str(e)}")
            return False

    def watch_input_directory(self):
        """Watch input directory for new transcript files"""
        print(f"Watching input directory: {self.input_dir}")
        print("Waiting for transcript files... (Press Ctrl+C to exit)")
        
        while True:
            try:
                for file in os.listdir(self.input_dir):
                    if file.endswith('_transcript.json'):
                        input_path = os.path.join(self.input_dir, file)
                        print(f"\nFound new transcript: {file}")
                        
                        # Get target language
                        print("\nAvailable target languages:")
                        print("ES - Spanish")
                        print("FR - French")
                        print("DE - German")
                        print("IT - Italian")
                        print("PT-PT - Portuguese")
                        print("RU - Russian")
                        print("JA - Japanese")
                        print("ZH - Chinese")
                        target_lang = input("\nEnter target language code: ").upper()
                        
                        if self.process_transcript(input_path, target_lang):
                            # Move or delete processed file
                            os.remove(input_path)
                            print(f"Processed and removed: {file}")
                
                time.sleep(5)  # Check every 5 seconds
                
            except KeyboardInterrupt:
                print("\nExiting service...")
                break
            except Exception as e:
                print(f"Error in watch loop: {str(e)}")
                time.sleep(5)

if __name__ == "__main__":
    auth_key = "bd006995-e700-4b10-8534-92668f452fbf:fx"  # Your DeepL API key
    service = TranslationService(auth_key)
    service.watch_input_directory()