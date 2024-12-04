import streamlit as st
from pytube import YouTube
from googletrans import Translator
import whisper
import os
import torch

def main():
    st.title("YouTube Video Dubbing Tool")
    
    # Input section
    st.header("1. Input YouTube URL")
    youtube_url = st.text_input("Enter YouTube URL:")
    
    target_language = st.selectbox(
        "Select target language",
        ["ja", "en", "ko", "zh-cn", "es", "fr", "de", "it", "ru", "ar"]
    )
    
    if st.button("Process Video"):
        if youtube_url:
            with st.spinner("Processing..."):
                try:
                    # Download YouTube audio
                    yt = YouTube(youtube_url)
                    st.info(f"Video Title: {yt.title}")
                    
                    # Download audio
                    audio_stream = yt.streams.filter(only_audio=True).first()
                    audio_file = audio_stream.download(filename="temp_audio")
                    
                    # Load Whisper model
                    model = whisper.load_model("base")
                    
                    # Transcribe
                    result = model.transcribe(audio_file)
                    transcription = result["text"]
                    
                    # Translate
                    translator = Translator()
                    translation = translator.translate(transcription, dest=target_language)
                    
                    # Display results
                    st.subheader("Original Transcription")
                    st.write(transcription)
                    
                    st.subheader("Translation")
                    st.write(translation.text)
                    
                    # Cleanup
                    if os.path.exists("temp_audio"):
                        os.remove("temp_audio")
                        
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter a YouTube URL")

if __name__ == "__main__":
    main()
