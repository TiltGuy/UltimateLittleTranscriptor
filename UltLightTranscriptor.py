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
    "--model_size", type=str, default="small", help="Size of the Whisper Model: tiny, base, small, medium, large"
)
parser.add_argument(
    "--language", type=str, default="en", help="Language of the audio file"
)
parser.add_argument(
    "--output_dir",
    type=str,
    default="./Transcriptions",
    help="Directory to save transcriptions",
)
parser.add_argument(
    "--input_dir",
    type=str,
    default="./Recordings",
    help="Directory to load audio files from",
)
parser.add_argument(
    "--verbose",
    action=argparse.BooleanOptionalAction,
    help="Whether to print verbose output during transcription",
)
parser.add_argument(
    "--auto_transcribe_ALL",
    action= argparse.BooleanOptionalAction,
    help="Whether to automatically transcribe all files in the input directory",
)
parser.add_argument(
    "--auto_transcribe",
    action=argparse.BooleanOptionalAction,
    help="Whether to automatically transcribe after recording",
)
args = parser.parse_args()
print(Fore.CYAN + "input dir = " + args.input_dir)
print(Fore.CYAN + "current dir = " + args.output_dir)
print(Fore.CYAN + "model size = " + args.model_size)
print(Fore.CYAN + "language = " + args.language)
print(Fore.CYAN + "verbose = " + str(args.verbose))
print(Fore.CYAN + "auto Transcription for ALL = " + str(args.auto_transcribe_ALL))
print(Fore.CYAN + "auto Transcription = " + str(args.auto_transcribe))


# def save_uploaded_file(uploaded_file, save_path):
#     with open(os.path.join(save_path, uploaded_file.name), "wb") as f:
#         f.write(uploaded_file)


def load_whisper_model(model_size=args.model_size):
    return whisper.load_model(model_size)


print(Fore.YELLOW + f"Loading Whisper model ({args.model_size})...")
model = load_whisper_model()
print(Fore.GREEN + "Model loaded successfully!\n")

# Create directories if they don't exist
os.makedirs(args.input_dir, exist_ok=True)
os.makedirs(args.output_dir, exist_ok=True)


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
            save_path = "./Transcriptions/"  # Directory to save transcriptions
            os.makedirs(save_path, exist_ok=True)

            print(
                Fore.YELLOW
                + f"\n[{idx}/{len(uploaded_files)}] Transcribing {uploaded_file.name}..."
            )
            transcribed_text = transcribe_audio(
                str(uploaded_file), language=args.language, verbose=args.verbose
            )
            output_file = os.path.join(args.output_dir, uploaded_file.stem + ".txt")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(transcribed_text)
            print(Fore.GREEN + f"✓ Saved to {output_file}")


def transcriptOneFile(filename):
    print(Fore.MAGENTA + "Transcription function called.")
    from pathlib import Path

    uploaded_file = Path("./Recordings/", filename)
    if not os.path.isfile(uploaded_file):
        print(Fore.RED + f"File {uploaded_file} does not exist.")
        return

    print(Fore.CYAN + f"Found audio files: {uploaded_file.name}")
    print(
        Fore.YELLOW
        + f"Transcribing {uploaded_file.name}..."
    )
    transcribed_text = transcribe_audio(
        str(uploaded_file), language=args.language, verbose=args.verbose
    )

    output_file = os.path.join(args.output_dir, uploaded_file.stem + ".txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(transcribed_text)
    print(Fore.GREEN + f"✓ Saved to {output_file}")


### THE MAIN FUNCTION FOR RECORDING WITH KEYBOARD INPUT
def main():
    printHelp()
    while True:

        try:
            is_Recording = True

            ### RECORDING PART
            if keyboard.is_pressed("t"):  # if key 't' is pressed
                print(Fore.GREEN + "'T' key pressed. Starting Recording...")
                print(Fore.YELLOW + "Press 'P' to stop Record...")
                #   THERE WE GO FOR THE RECORDING
                os.makedirs("Recordings", exist_ok=True)
                CHUNK = 1024  # Record in chunks of 1024 samples
                p = pyaudio.PyAudio()  # Create an interface to PortAudio
                stream = p.open(
                    format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    input=True,
                    frames_per_buffer=CHUNK,
                )

                frames = []  # Initialize array to store frames
                while is_Recording == True:

                    data = stream.read(CHUNK)
                    frames.append(data)
                    sys.stdout.write(
                        Fore.CYAN
                        + f"\rRecording... {len(frames)} chunks ({len(frames) * CHUNK / 44100:.1f}s)"
                    )
                    sys.stdout.flush()
                    if keyboard.is_pressed("p"):  # if key 't' is pressed
                        print(Fore.YELLOW + "\n'P' key pressed. Stopping Recording...")
                        is_Recording = False
                        # stop and close the stream

                stream.close()
                p.terminate()

                # save the recorded file
                date_time = time.strftime("%Y%m%d-%H%M%S")
                name = "recording_" + date_time + ".wav"
                print(Fore.YELLOW + f"Saving recording as {name}...")
                wf = wave.open(name, "wb")
                wf.setnchannels(1)
                wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
                wf.setframerate(44100)
                wf.writeframes(b"".join(frames))
                wf.close()
                shutil.move(name, "./Recordings/" + name)
                print(Fore.GREEN + f"✓ Recording saved to ./Recordings/{name}")
                
                if args.auto_transcribe_ALL:
                    # THERE WE GO FOR THE TRANSCRIPTION FOR ALL
                    launchTranscriptionForAll()
                if args.auto_transcribe:
                    # THERE WE GO FOR THE TRANSCRIPTION
                    transcriptOneFile(name)
                    
                printHelp()
                    
                

            ### DELETION PART but just the transcriptions
            if keyboard.is_pressed("w"):  # if key 'w' is pressed
                print(
                    Fore.RED
                    + "'W' key pressed. Are you sure you want to delete all transcriptions? (y/n)"
                )
                is_Deleting = True
                while is_Deleting == True:
                    try:
                        if keyboard.is_pressed("y"):  # if key 'y' is pressed
                            if os.path.exists(args.output_dir):
                                ##Remove all files in the directory
                                for filename in os.listdir(args.output_dir):
                                    if filename.endswith(".txt"):
                                        print(Fore.YELLOW + f"Deleting {filename}...")
                                        os.remove(
                                            os.path.join(args.output_dir, filename)
                                        )
                                        THREAD_SLEEP = 0.1
                                        time.sleep(THREAD_SLEEP)
                                print(Fore.GREEN + "✓ All transcriptions deleted.")
                                is_Deleting = False
                        if keyboard.is_pressed("n"):  # if key 'n' is pressed
                            print(Fore.RED + "Aborting deletion...")
                            is_Deleting = False
                    except:
                        print(Fore.RED + "Aborting deletion...")
                        is_Deleting = False
                printHelp()
                
                
            ### DELETION PART but just the recordings
            if keyboard.is_pressed("q"):  # if key 'q' is pressed
                print(
                    Fore.RED
                    + "'Q' key pressed. Are you sure you want to delete all the audio-recordings? (y/n)"
                )
                is_Deleting = True
                while is_Deleting == True:
                    try:
                        if keyboard.is_pressed("y"):  # if key 'y' is pressed
                            if os.path.exists(args.input_dir):
                                ##Remove all files in the directory
                                for filename in os.listdir(args.input_dir):
                                    if filename.endswith(".wav") or filename.endswith(".mp3") or filename.endswith(".m4a"):
                                        print(Fore.YELLOW + f"Deleting {filename}...")
                                        os.remove(
                                            os.path.join(args.input_dir, filename)
                                        )
                                        THREAD_SLEEP = 0.1
                                        time.sleep(THREAD_SLEEP)
                                print(Fore.GREEN + "✓ All Recordings deleted.")
                                is_Deleting = False
                        if keyboard.is_pressed("n"):  # if key 'n' is pressed
                            print(Fore.RED + "Aborting deletion...")
                            is_Deleting = False
                    except:
                        print(Fore.RED + "Aborting deletion...")
                        is_Deleting = False
                printHelp()
                
                
            ### Transcription PART for all files in the folder
            if keyboard.is_pressed("o"):  # if key 'o' is pressed
                launchTranscriptionForAll()
                printHelp()
            if keyboard.is_pressed("x"):  # if key 'x' is pressed
                print(Fore.RED + "'x' key pressed. aborting anything (even my life)...")
                keyboard.unhook_all() # clean keyboard shenanigans
                sys.exit(0)  # terminate the program immediately
        except:
            keyboard.unhook_all() # clean keyboard shenanigans
            break

def launchTranscriptionForAll():
    print(Fore.MAGENTA + "Transcription started...")
    transcriptZaWarudo()
    print(Fore.GREEN + "Transcription finished.")

def printHelp():
    THREAD_SLEEP = 1
    time.sleep(THREAD_SLEEP)
    print("")
    print("//----------------------------\\\\")
    print(Fore.CYAN + "UltLight Transcriptor by UltLight")
    print("//----------------------------\\\\\n")
    print(Fore.GREEN + "Press 'T' to start Record...")
    print(Fore.BLUE + "Press 'O' to transcribe all recordings...")
    print(Fore.LIGHTYELLOW_EX + "Press 'Q' to wipe all previous recordings...")
    print(Fore.LIGHTYELLOW_EX + "Press 'W' to wipe all previous transcriptions...")
    print(
        Fore.RED + "Press 'X' to exit."
    )  # if user presses a key other than the given key the loop will break


if __name__ == "__main__":
    try:
        main()
    finally:
        keyboard.unhook_all() # clean keyboard shenanigans
        print(Fore.RED + "\nExiting... Goodbye!")
        sys.exit(0)  # terminate the program immediately
