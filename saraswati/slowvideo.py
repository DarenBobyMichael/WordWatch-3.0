from pydub import AudioSegment

def slow_down_audio(input_file, output_file, speed_factor):
    # Load the audio file
    audio = AudioSegment.from_wav(input_file)

    # Adjust the frame rate to slow down the audio
    new_frame_rate = int(audio.frame_rate / speed_factor)
    print(audio.frame_rate,new_frame_rate)
    slowed_audio = audio.set_frame_rate(new_frame_rate)


    # Export the slowed down audio to a new file
    slowed_audio.export(output_file, format="wav")

if __name__ == "__main__":
    input_file = "Audio/video_audio.wav"  # Provide the path to your input WAV file
    output_file = "output_slowed.wav"  # Output file name
    speed_factor = 4  # Change this to adjust the speed factor, e.g., 2 for half speed

    slow_down_audio(input_file, output_file, speed_factor)
    print("Audio slowed down and saved to", output_file)
