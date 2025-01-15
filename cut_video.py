import subprocess

def trim_video(input_path, output_path, start_time, end_time):
    """
    Trims a video using ffmpeg from start_time to end_time.

    :param input_path: Path to the input video file.
    :param output_path: Path to save the trimmed video.
    :param start_time: Start time in seconds (e.g., 10).
    :param end_time: End time in seconds (e.g., 20).
    """
    try:
        # Construct the ffmpeg command
        command = [
            "ffmpeg",
            "-i", input_path,
            "-ss", str(start_time),
            "-to", str(end_time),
            "-c:v", "copy",
            "-c:a", "copy",
            output_path
        ]
        # Run the command
        subprocess.run(command, check=True)
        print(f"Video trimmed and saved to {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during video trimming: {e}")

# Example usage
input_file = input("Enter the path to the video file: ")
output_file = input("Enter the output file name (e.g., trimmed_video.mp4): ")
start = float(input("Enter the start time in seconds: "))
end = float(input("Enter the end time in seconds: "))
trim_video(input_file, output_file, start, end)