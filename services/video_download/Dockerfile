FROM python:3.9-slim

WORKDIR /usr/src/app

# Install ffmpeg and aria2 for faster downloads
RUN apt-get update &&     apt-get install -y ffmpeg aria2 &&     rm -rf /var/lib/apt/lists/*

COPY video_download_service.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p downloads

CMD ["python", "video_download_service.py"]
