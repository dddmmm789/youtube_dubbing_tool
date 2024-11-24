import ffmpeg
import os
import sys

def extract_audio(input_video_path, output_audio_path):
    """
    Extracts audio from an MKV file and saves it to the specified output path.
    """
    try:
        ffmpeg.input(input_video_path).output(output_audio_path, **{'y': None}).run()
        print(f"\nAudio extracted successfully to {output_audio_path}")
        return True
    except ffmpeg.Error as e:
        print(f"\nAn error occurred while extracting audio: {e}")
        return False

def wait_for_file_and_proceed():
    """
    Waits for the latest MKV file in the input folder and converts it to audio.
    Exits after processing one file.
    """
    print("=== Starting audio extraction service ===")
    
    # Get paths from environment variables
    video_folder = os.getenv("VIDEO_FOLDER")
    audio_output_folder = os.getenv("AUDIO_OUTPUT_FOLDER")

    print(f"\nMonitoring directories:")
    print(f"Input folder: {video_folder}")
    print(f"Output folder: {audio_output_folder}")

    # Check if the video folder exists
    if not os.path.exists(video_folder):
        print(f"Error: The folder '{video_folder}' does not exist.")
        return

    # Ensure the audio output folder exists
    os.makedirs(audio_output_folder, exist_ok=True)

    print("\nLooking for .mkv files...")

    # Find the latest .mkv file
    latest_file = None
    latest_time = 0

    for file_name in os.listdir(video_folder):
        if file_name.endswith(".mkv"):
            file_path = os.path.join(video_folder, file_name)
            file_time = os.path.getmtime(file_path)

            if file_time > latest_time:
                latest_time = file_time
                latest_file = file_name

    if latest_file:
        print(f"\nProcessing file: {latest_file}")
        input_path = os.path.join(video_folder, latest_file)
        output_path = os.path.join(audio_output_folder, f"{os.path.splitext(latest_file)[0]}.wav")
        
        if extract_audio(input_path, output_path):
            print("\n=== Audio extraction completed successfully ===")
        else:
            print("\n=== Audio extraction failed ===")
    else:
        print("\nNo .mkv files found in the input directory.")

    print("\nExiting service.")
    sys.exit(0)

if __name__ == "__main__":
    wait_for_file_and_proceed()
