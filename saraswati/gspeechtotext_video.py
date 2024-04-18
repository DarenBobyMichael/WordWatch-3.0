from google.cloud import speech_v1p1beta1 as speech
import os
from ml2en import ml2en
import re
import subprocess
import videotoaudio

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "saraswati/google_cred.json"
def transcribe_malayalam_audio(video_name):

        video_path="saraswati/uploads/"+video_name
        videotoaudio.extract_audio_from_video(video_path,"saraswati/Audio/video_audio.wav")
        audio_path='saraswati/Audio/video_audio.wav'
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

        transcripts = []
        
        for result in response.results:
            transcripts.append(result.alternatives[0].transcript)
        print(transcripts[0])

        return transcripts[0]
    

