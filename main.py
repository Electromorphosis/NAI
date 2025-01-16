import cv2
import time
import tkinter as tk
from PIL import Image, ImageTk
import simpleaudio as sa
from threading import Thread

# Global variables
start_program = False
face_cascPath = "./pretrained/face_detector.xml"
eye_cascPath = "./pretrained/eye_detector.xml"
font = cv2.FONT_HERSHEY_SIMPLEX

face_filter = cv2.CascadeClassifier(face_cascPath)
eye_filter = cv2.CascadeClassifier(eye_cascPath)
if face_filter.empty() or eye_filter.empty():
    raise IOError("Where is my filter?!?!!")

eyes_are_open = False
eyes_closed_warning = False
start_time = time.time()
prev_time = 0
fps = 0
current_frame = 0
warn_frame = 0
stop_frame = -1
previous_frame = None
warn_sign_on = False
social_credit_score = 0
early_ret_false_positive_buffer = True
video_number = 2

# Initialize video and camera streams
cap = cv2.VideoCapture('./downloads/start.jpg')
camera = cv2.VideoCapture(0)

def audio(filepath):
    """
    Play audio from the specified file and manage playback based on global state.

    Args:
        filepath (str): Path to the audio file.
    """
    wave_obj = sa.WaveObject.from_wave_file(filepath)
    play_obj = wave_obj.play()
    is_playing = True
    global eyes_closed_warning

    while play_obj.is_playing():
        if eyes_closed_warning:
            play_obj.pause()
            is_playing = False
        elif not is_playing:
            play_obj.resume()
            is_playing = True

        time.sleep(0.1)  # Delay to reduce CPU usage


def alarm_sound():
    """
    Continuously manage the alarm sound playback based on the eyes_closed_warning global state.

    The alarm plays when `eyes_closed_warning` is True and pauses otherwise.
    """
    global eyes_closed_warning
    global start_program

    while True:
        wave_obj = sa.WaveObject.from_wave_file('./educational_materials/alarm_improved.wav')
        is_playing = False
        play_obj = wave_obj.play()
        play_obj.pause()

        while play_obj.is_playing():
            if eyes_closed_warning:
                if not is_playing:
                    play_obj.resume()
                    is_playing = True
            else:
                play_obj.pause()
                is_playing = False

            time.sleep(0.1)  # Delay to reduce CPU usage


def update_video():
    """
    Update the main video feed displayed on the canvas.

    - Manages the playback of video and ensures synchronization with the `eyes_closed_warning` state.
    - Displays various overlays, such as the current frame number, warning state, and social credit score.
    - Handles video switching when the current video finishes.
    """
    global eyes_closed_warning
    global previous_frame
    global current_frame
    global start_program
    global warn_frame
    global warn_sign_on
    global alarm_thread
    global social_credit_score
    global early_ret_false_positive_buffer
    global video_number
    global cap

    if eyes_closed_warning:
        cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)

    ret, frame = cap.read()

    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (screen_width, screen_height))

        if start_program:
            if not eyes_closed_warning:
                current_frame += 1

            if current_frame > 50:
                early_ret_false_positive_buffer = False

            # Display text overlays on the video frame
            cv2.putText(frame, f'Current frame: {int(current_frame)}', (10, 30), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, f'Warn frame: {int(warn_frame)}', (10, 60), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, f'Eyes open in the moment? {str(eyes_are_open)}', (10, 90), font, 1, (0, 255, 0), 2,
                        cv2.LINE_AA)
            cv2.putText(frame, f'Social Credits: {int(social_credit_score)}', (10, 120), font, 1, (0, 255, 0), 2,
                        cv2.LINE_AA)

            # Handle warnings for closed eyes
            if eyes_closed_warning:
                if not alarm_thread.is_alive():
                    alarm_thread.start()
                if warn_sign_on:
                    warn_sign_on = False
                else:
                    cv2.putText(frame, "EYES ARE CLOSED!!!", (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 0, 0), 10)
                    warn_sign_on = True

        # Render the frame on the video canvas
        frame_img = ImageTk.PhotoImage(Image.fromarray(frame))
        video_canvas.create_image(0, 0, anchor=tk.NW, image=frame_img)
        video_canvas.image = frame_img

    else:
        if not early_ret_false_positive_buffer:
            print("RET FALSE ; " + str(cap.get(cv2.CAP_PROP_FRAME_COUNT)))

            # Handle video completion and loop to the next video
            social_credit_score += 1
            early_ret_false_positive_buffer = True
            current_frame = 0
            video_number = 2 if video_number == 1 else 1
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart video
            cap = cv2.VideoCapture(f'./educational_materials/{video_number}.mp4')
            audio_thread = Thread(target=audio, args=(f'./educational_materials/{video_number}.wav',), daemon=True)
            audio_thread.start()

    root.after(5, update_video)


def update_camera():
    """
    Update the live camera feed displayed on the small canvas.

    - Captures frames from the live camera feed and processes them for face and eye detection.
    - Calculates and displays the FPS on the video feed.
    - Tracks the state of eyes (open or closed) and adjusts the warning frame counter accordingly.
    - Draws rectangles around detected faces and valid eyes, ensuring eyes are filtered to only those within faces.
    """
    ret, frame = camera.read()
    current_time = time.time()

    if ret:
        # Convert frame to RGB for Tkinter compatibility
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        global prev_time
        fps = 1 / (current_time - prev_time)  # Calculate frames per second
        prev_time = current_time

        # Flip the frame horizontally for a mirror effect
        frame = cv2.flip(frame, 1)

        # Convert frame to grayscale for face and eye detection
        global face_filter
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces and eyes
        face_rects = face_filter.detectMultiScale(gray_frame, 1.3, 5)
        eye_rects = eye_filter.detectMultiScale(gray_frame, 1.3, 5)

        # Filter eyes to retain only those within detected faces
        filtered_eyes = [
            (x_eye, y_eye, w_eye, h_eye)
            for (x_face, y_face, w_face, h_face) in face_rects
            for (x_eye, y_eye, w_eye, h_eye) in eye_rects
            if x_face < x_eye < x_face + w_face and y_face < y_eye < y_face + h_face and
               (x_eye + w_eye) < (x_face + w_face) and (y_eye + h_eye) < (y_face + h_face)
        ]
        eye_rects = filtered_eyes

        # Draw rectangles around detected faces and valid eyes
        for (x_face, y_face, w_face, h_face) in face_rects:
            cv2.rectangle(frame, (x_face, y_face), (x_face + w_face, y_face + h_face), (0, 255, 255), 3)

        for (x_eye, y_eye, w_eye, h_eye) in eye_rects:
            cv2.rectangle(frame, (x_eye, y_eye), (x_eye + w_eye, y_eye + h_eye), (0, 255, 0), 3)

        # Update eye state and warning frame counter
        global eyes_are_open
        global warn_frame
        global eyes_closed_warning
        if len(eye_rects) == 0:
            eyes_are_open = False
            warn_frame = min(warn_frame + 1, 5)  # Cap warn_frame at 5
            if warn_frame == 5 and not eyes_closed_warning:
                eyes_closed_warning = True
        else:
            eyes_are_open = True
            warn_frame = max(warn_frame - 1, 0)  # Prevent warn_frame from going negative
            if warn_frame == 0 and eyes_closed_warning:
                eyes_closed_warning = False

        # Display FPS on the video feed
        cv2.putText(frame, f'FPS: {int(fps)}', (10, 30), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # Resize and render the frame on the small canvas
        frame = cv2.resize(frame, (small_canvas_width - 4, small_canvas_height - 4))
        frame_img = ImageTk.PhotoImage(Image.fromarray(frame))
        small_canvas.create_image(0, 0, anchor=tk.NW, image=frame_img)
        small_canvas.image = frame_img

    # Schedule the next frame update
    root.after(105, update_camera)


def update_small_canvas(event):
    """
    Update the size and position of the small canvas based on the main window dimensions.

    - Resizes the small canvas to be one-quarter the width and height of the main window.
    - Positions the small canvas at the bottom-right corner of the main window.

    Args:
        event: The event object triggered by window resize or other UI events.
    """
    global small_canvas_width, small_canvas_height

    # Calculate new dimensions for the small canvas
    small_canvas_width = screen_width // 4
    small_canvas_height = screen_height // 4

    # Place the small canvas at the bottom-right corner of the main window
    small_canvas.place(x=screen_width - small_canvas_width, y=screen_height - small_canvas_height)


# Initialize alarm thread
alarm_thread = Thread(target=alarm_sound, daemon=True)

# Initialize tkinter window
root = tk.Tk()
root.title("Video and Camera Feed")

# Set window size and fullscreen attributes
root.geometry("800x600")
root.attributes("-fullscreen", True)

# Get screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Define dimensions for small canvas
small_canvas_width = screen_width // 4
small_canvas_height = screen_height // 4

# Create the main video canvas (filling entire screen)
video_canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg="black")
video_canvas.pack(fill=tk.BOTH, expand=True)

# Create the smaller camera canvas (bottom-right corner)
small_canvas = tk.Canvas(root, width=small_canvas_width, height=small_canvas_height, bg="white", bd=2)
small_canvas.place(x=screen_width - small_canvas_width, y=screen_height - small_canvas_height)

# Bind window resize event to update the small canvas size and position
root.bind("<Configure>", update_small_canvas)

# Start video and camera update loops
update_video()
update_camera()

# Define keyboard controls for the application
def keyboard_controls(event):
    """
    Handles keyboard input for controlling the video and application behavior.

    This function processes different key events:
    - 'q' key: Closes the application.
    - 'space' key: Starts video playback from the beginning, if not already started,
      and initializes the associated audio.

    Args:
        event (tkinter.Event): The keyboard event that triggered the function.
    """
    global current_frame, start_program, cap

    # Exit application on 'q' key press
    if event.char == "q":
        root.destroy()

    # Start video playback on 'space' key press
    if event.keysym == "space":
        if not start_program:
            start_program = True
            current_frame = 0
            cap = cv2.VideoCapture('./educational_materials/2.mp4')

            # Start the audio thread
            audio_thread = Thread(target=audio, args=('./educational_materials/2.wav',), daemon=True)
            audio_thread.start()


# Bind keyboard controls
root.bind("<Key>", keyboard_controls)

# Start the tkinter main loop
root.mainloop()

# Release resources after the main loop ends
cap.release()
camera.release()
cv2.destroyAllWindows()