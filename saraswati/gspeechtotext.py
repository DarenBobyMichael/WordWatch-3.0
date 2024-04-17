from google.cloud import speech_v1p1beta1 as speech
import os
from ml2en import ml2en
import re
import subprocess

def convert_stereo_to_mono(input_filename, output_filename):
    subprocess.run(["ffmpeg", "-i", input_filename, "-ac", "1", output_filename])

def convert_to_wav(input_filename):
    if not re.match(r".*\.wav$", input_filename):
        output_filename = os.path.splitext(input_filename)[0] + ".wav"
        # Use ffmpeg to convert the file to .wav
        subprocess.run(["ffmpeg", "-i", input_filename, output_filename])
        print(f"File '{input_filename}' has been converted to '{output_filename}'.")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "saraswati/google_cred.json"
def transcribe_malayalam_audio():
    audio_path=input('Enter audio file name: ')
    audio_path='saraswati/Audio/'+audio_path
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

    return transcripts[0]

# Replace with the path to your Malayalam audio file

audio_file_path='dheeraj.wav'
