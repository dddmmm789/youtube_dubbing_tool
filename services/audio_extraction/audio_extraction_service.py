import ffmpeg
import os

def extract_audio(input_video_path, output_audio_path):
    """
    Extracts audio from an MKV file and saves it to the specified output path.
    """
    try:
        ffmpeg.input(input_video_path).output(output_audio_path).run()
        print(f"Audio extracted successfully to {output_audio_path}")
    except ffmpeg.Error as e:
        print(f"An error occurred while extracting audio: {e}")

def wait_for_file_and_proceed():
    """
    Waits for the user to place the latest MKV file in the 'to_extract_audio' folder.
    Once the file is present, it will convert it to audio.
    """
    video_folder = '/Users/danm/youtube_dubbing_project/services/video_download/downloads/to_extract_audio'
    audio_output_folder = '/Users/danm/youtube_dubbing_project/services/audio_extraction/audio_files'

    # Check if the video folder exists
    if not os.path.exists(video_folder):
        print(f"Error: The folder '{video_folder}' does not exist.")
        return

    # Ensure the audio output folder exists
    os.makedirs(audio_output_folder, exist_ok=True)

    # Find the latest .mkv file in the folder based on modification time
    video_file = None
    latest_time = 0  # Initialize the time to compare

    for file_name in os.listdir(video_folder):
        if file_name.endswith('.mkv'):
            file_path = os.path.join(video_folder, file_name)
            file_time = os.path.getmtime(file_path)  # Get last modification time

            if file_time > latest_time:
                latest_time = file_time
                video_file = file_name

    if not video_file:
        print(f"Please add an MKV file to the folder {video_folder}.")
        input("Press Enter when the file is ready...")

    # Wait until the latest file is added
    while not video_file:
        for file_name in os.listdir(video_folder):
            if file_name.endswith('.mkv'):
                file_path = os.path.join(video_folder, file_name)
                file_time = os.path.getmtime(file_path)
                if file_time > latest_time:
                    latest_time = file_time
                    video_file = file_name
                    break
        if not video_file:
            input(f"Still waiting for the file. Press Enter once it's ready...")

    # Once the file is ready, proceed with the audio extraction
    input_video_path = os.path.join(video_folder, video_file)
    output_audio_path = os.path.join(audio_output_folder, f"{os.path.splitext(video_file)[0]}.wav")
    
    print(f"File found: {video_file}. Proceeding with audio extraction.")
    extract_audio(input_video_path, output_audio_path)


# Example usage
if __name__ == "__main__":
    wait_for_file_and_proceed()
