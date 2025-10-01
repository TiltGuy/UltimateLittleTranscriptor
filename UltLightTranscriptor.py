import os
import sys
import whisper
import argparse
import keyboard
import pyaudio
import wave
import time
import shutil
from colorama import Fore, init

init(autoreset=True)

parser = argparse.ArgumentParser(
    description="Transcribe audio files using Whisper model."
)
parser.add_argument(
    "--model_size", type=str, default="base", help="Size of the Whisper Model"
)
parser.add_argument(
    "--language", type=str, default="en", help="Language of the audio file"
)
parser.add_argument(
    "--output_dir",
    type=str,
    default="./Transcriptions",
    help="Directory containing audio files to transcribe",
)
parser.add_argument(
    "--verbose",
    type=bool,
    default=False,
    help="Whether to print verbose output during transcription",
)
args = parser.parse_args()
print(Fore.CYAN + "current dir = " + args.output_dir)
print(Fore.CYAN + "model size = " + args.model_size)
print(Fore.CYAN + "language = " + args.language)
print(Fore.CYAN + "verbose = " + str(args.verbose))


# def save_uploaded_file(uploaded_file, save_path):
#     with open(os.path.join(save_path, uploaded_file.name), "wb") as f:
#         f.write(uploaded_file)


def load_whisper_model(model_size=args.model_size):
    return whisper.load_model(model_size)


print(Fore.YELLOW + f"Loading Whisper model ({args.model_size})...")
model = load_whisper_model()
print(Fore.GREEN + "Model loaded successfully!\n")


def transcribe_audio(file_path, language="en", verbose=args.verbose):
    # transcribe the audio file using Whisper model specified language (or not hihihi)
    result = model.transcribe(file_path, language=language, verbose=verbose)
    # TODO: handle json for timestamping later
    return result["text"]


def transcriptZaWarudo():
    print(Fore.MAGENTA + "Transcription function called.")
    from pathlib import Path

    uploaded_files = [
        files
        for files in Path("./Recordings/").iterdir()
        if Path(files).suffix in [".mp3", ".wav", ".m4a"]
    ]

    print(Fore.CYAN + f"Found {len(uploaded_files)} audio files: {uploaded_files}")

    if not uploaded_files:
      try:
        print(Fore.YELLOW + "No audio files found in the input directory.")
        print(Fore.YELLOW + "Checking current directory for audio files...")
        uploaded_files = [
          files
          for files in Path("./Recordings/").iterdir()
            if (files).suffix in [".mp3", ".wav", ".m4a"]
        ] 
      except:
        print(Fore.RED + "Input directory not found.")
        print(Fore.RED + "No audio files found in the current directory.")
        return

    else:
        for idx, uploaded_file in enumerate(uploaded_files, 1):
            save_path = "./Recordings/"  # Directory to save transcriptions
            os.makedirs(save_path, exist_ok=True)

            print(Fore.YELLOW + f"\n[{idx}/{len(uploaded_files)}] Transcribing {uploaded_file.name}...")
            transcribed_text = transcribe_audio(
                str(uploaded_file), language=args.language, verbose=args.verbose
            )
            output_file = os.path.join(args.output_dir, uploaded_file.stem + ".txt")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(transcribed_text)
            print(Fore.GREEN + f"✓ Saved to {output_file}")


def main():
    print(Fore.GREEN + "Press 'T' to start Record...")
    print(Fore.RED + "Press 'X' to exit.")
    while True:
        try:
            is_Recording = True
            if (keyboard.is_pressed("t")):  # if key 't' is pressed
                print(Fore.GREEN + "'T' key pressed. Starting Recording...")
                print(Fore.YELLOW + "Press 'P' to stop Record...")
                #   THERE WE GO FOR THE RECORDING
                os.makedirs("Recordings", exist_ok=True)
                CHUNK = 1024  # Record in chunks of 1024 samples
                p = pyaudio.PyAudio()  # Create an interface to PortAudio
                stream = p.open(format = pyaudio.paInt16,
                                channels = 1,
                                rate = 44100,
                                input = True,
                                frames_per_buffer = CHUNK)
                
                frames = []  # Initialize array to store frames
                while is_Recording == True:

                  data = stream.read(CHUNK)
                  frames.append(data)
                  sys.stdout.write(Fore.CYAN + f"\rRecording... {len(frames)} chunks ({len(frames) * CHUNK / 44100:.1f}s)")
                  sys.stdout.flush()
                  if keyboard.is_pressed("p"):  # if key 't' is pressed
                      print(Fore.YELLOW + "\n'P' key pressed. Stopping Recording...")
                      is_Recording = False
                      # stop and close the stream
                    
                stream.close()
                p.terminate()

                #save the recorded file
                date_time = time.strftime("%Y%m%d-%H%M%S")
                name = "recording_"+date_time+".wav"
                print(Fore.YELLOW + f"Saving recording as {name}...")
                wf = wave.open(name, 'wb')
                wf.setnchannels(1)
                wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
                wf.setframerate(44100)
                wf.writeframes(b''.join(frames))
                wf.close()
                shutil.move(name, "./Recordings/"+name)
                print(Fore.GREEN + f"✓ Recording saved to ./Recordings/{name}")
                # THERE WE GO FOR THE TRANSCRIPTION
                print(Fore.MAGENTA + "Transcription started...")
                transcriptZaWarudo()
                print(Fore.GREEN + "Transcription finished.")
                break  # exit the loop after transcription

            if keyboard.is_pressed("x"):  # if key 't' is pressed
                print(Fore.RED + "'x' key pressed. aborting transcription...")
                break  # exit the loop after transcription
        except:
            break  # if user presses a key other than the given key the loop will break



if __name__ == "__main__":
    main()
