import subprocess

def extract_audio_from_video(input_video, output_wav):
    subprocess.run(["ffmpeg", "-i", input_video, "-vn", "-acodec", "pcm_s16le", "-ar", "48000", "-ac", "1", output_wav])

