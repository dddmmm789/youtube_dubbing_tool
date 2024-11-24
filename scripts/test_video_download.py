import sys
import os

# Add the parent directory of 'services' to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.video_download.video_download_service import download_video

# Test the video download with a sample URL (replace with an actual YouTube URL)
youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
output_path = "data/videos"  # Specify where to save the video

video_path = download_video(youtube_url, output_path)
if video_path:
    print(f"Video downloaded successfully: {video_path}")
else:
    print("Failed to download video.")
