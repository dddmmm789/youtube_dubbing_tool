import subprocess
import os

def download_video(url, output_dir):
    command = [
        'yt-dlp',
        '--format', 'bestvideo+bestaudio',
        '--merge-output-format', 'mkv',
        '--external-downloader', 'aria2c',
        '--external-downloader-args', 'aria2c:-x 16 -s 16 -k 1M',  # 16 connections
        '-o', f'{output_dir}/%(id)s_%(title)s.%(ext)s',
        url
    ]
    
    print(f'Downloading video from: {url}')
    result = subprocess.run(command)
    
    if result.returncode == 0:
        print('Download successful!')
    else:
        print('Download failed!')

if __name__ == '__main__':
    url = os.getenv('YOUTUBE_URL')
    output_dir = os.getenv('OUTPUT_DIR')
    download_video(url, output_dir)
