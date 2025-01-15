import subprocess
import os



def modify_pitch(input_file, output_file, pitch_shift_semitones):
    """
    Modify the pitch of the audio in an MP4 file without affecting the video.

    Args:
        input_file (str): Path to the input MP4 file.
        output_file (str): Path to save the modified MP4 file.
        pitch_shift_semitones (int): Number of semitones to shift the pitch (+ for higher, - for lower).
    """
    # FFmpeg command to modify the pitch
    # asetrate changes the audio pitch by modifying the audio rate without affecting the speed.
    pitch_factor = 2 ** (pitch_shift_semitones / 12.0)  # Convert semitones to pitch factor
    cmd = [
        "ffmpeg",
        "-i", input_file,  # Input file
        "-filter:a", f"asetrate={44100 * pitch_factor},atempo=1",  # Apply pitch shift
        "-c:v", "copy",  # Copy the video stream without re-encoding
        "-c:a", "aac",  # Use AAC for audio codec
        "-b:a", "192k",  # Audio bitrate
        output_file
    ]

    subprocess.run(cmd, check=True)
    print(f"Pitch modified and saved to {output_file}")


def choose_file_from_directory(directory_path):
    # List all files in the specified directory
    try:
        files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

        if not files:
            print("No files found in the directory.")
            return None

        # Display the list of files with numbers
        print("Please choose a file by its number:")
        for idx, file in enumerate(files, start=1):
            print(f"{idx}. {file}")

        # Prompt the user to select a file by number
        choice = int(input("Enter the number of the file you want to choose: "))

        # Check if the choice is valid
        if 1 <= choice <= len(files):
            selected_file = files[choice - 1]
            print(f"You selected: {selected_file}")
            return os.path.join(directory_path, selected_file)
        else:
            print("Invalid choice.")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None


# Example usage
downloads_folder = os.path.expanduser(".\downloads")  # Path to Downloads folder
chosen_file = choose_file_from_directory(downloads_folder)
if chosen_file:
    print(f"Chosen file path: {chosen_file}")
# Example usage
modify_pitch(chosen_file, "output_video_with_modified_pitch.mp4", 4)  # Shift pitch by +4 semitones
