FROM python:3.9-slim

WORKDIR /usr/src/app

# Install ffmpeg
RUN apt-get update &&     apt-get install -y ffmpeg &&     rm -rf /var/lib/apt/lists/*

# Add this line to force rebuild
RUN echo 'Rebuild: 1'

COPY audio_extraction_service.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p audio_files

CMD ["python", "audio_extraction_service.py"]
