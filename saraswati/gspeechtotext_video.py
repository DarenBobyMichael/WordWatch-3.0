from google.cloud import speech_v1p1beta1 as speech
import os
from ml2en import ml2en
import re
import subprocess
import saraswati.videotoaudio

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "saraswati/google_cred.json"
def transcribe_malayalam_audio(video_name):
    video_path = "saraswati/uploads/" + video_name
    saraswati.videotoaudio.extract_audio_from_video(video_path, f"saraswati/Audio/{video_name.split('.')[0]}.wav")
    audio_path = f"saraswati/Audio/{video_name.split('.')[0]}.wav"
    client = speech.SpeechClient()
    with open(audio_path, "rb") as audio_file:
        content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=48000,
        language_code="ml-IN",  # Malayalam language code
    )
    response = client.recognize(config=config, audio=audio)
    # Join all transcripts into a single string
    full_transcript = " ".join([result.alternatives[0].transcript for result in response.results])
    print(full_transcript)  # If you want to print the full transcript
    
    return full_transcript

