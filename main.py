import cv2
import time
import tkinter as tk
from PIL import Image, ImageTk
import simpleaudio as sa
from threading import Thread

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

# Open video file and camera
cap = cv2.VideoCapture('./downloads/start.jpg')  # Replace with your video path
camera = cv2.VideoCapture(0)  # 0 = default webcam

def audio(filepath):
    # Load the audio file once
    wave_obj = sa.WaveObject.from_wave_file(filepath)
    play_obj = wave_obj.play()
    is_playing = True
    global eyes_closed_warning
    while play_obj.is_playing():
        if eyes_closed_warning:
            # print("Paused!")
            play_obj.pause()
            is_playing = False
        else:
            if not is_playing:
                # print("Resumed!")
                play_obj.resume()
                is_playing = True

        time.sleep(0.1)  # Small delay to avoid busy-waiting

def alarm_sound():
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
                    # print("Paused!")
                    play_obj.resume()
                    is_playing = True
            else:
                    # print("Resumed!")
                    play_obj.pause()
                    is_playing = False

            time.sleep(0.1)  # Small delay to avoid busy-waiting


alarm_thread = Thread(target=alarm_sound, daemon=True)


# Function to update the main video feed
def update_video():
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
            cv2.putText(frame, f'Current frame: {int(current_frame)}', (10, 30), font, 1,
                        (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, f'Warn frame: {int(warn_frame)}', (10, 60), font, 1,
                        (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, f'Eyes open in the moment? {str(eyes_are_open)}', (10, 90), font, 1,
                        (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, f'Social Credits: {int(social_credit_score)}', (10, 120), font, 1,
                        (0, 255, 0), 2, cv2.LINE_AA)
            if eyes_closed_warning:
                if not alarm_thread.is_alive():
                    alarm_thread.start()
                if warn_sign_on:
                    warn_sign_on = False
                else:
                    cv2.putText(frame, "EYES ARE CLOSED!!!", (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 5,
                                (255, 0, 0), 10)
                    warn_sign_on = True




            # print("Eyes warn frame = " + str(warn_frame))
        # Render final frame
        frame_img = ImageTk.PhotoImage(Image.fromarray(frame))
        video_canvas.create_image(0, 0, anchor=tk.NW, image=frame_img)
        video_canvas.image = frame_img

    else:
        if not early_ret_false_positive_buffer:
            print("RET FALSE ; " + str(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
            # If video is finished (ret is nonzero)
            social_credit_score += 1
            early_ret_false_positive_buffer = True
            current_frame = 0
            if video_number == 1:
                video_number = 2
            else:
                video_number = 1
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart video when it ends
            cap = cv2.VideoCapture('./educational_materials/' + str(video_number) + '.mp4')
            audio_thread = Thread(target=audio, args=('./educational_materials/' + str(video_number) + '.wav',), daemon=True)
            audio_thread.start()

    root.after(5, update_video)

# Function to update the live camera feed
def update_camera():
    ret, frame = camera.read()
    current_time = time.time()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


        global prev_time
        fps = 1 / (current_time - prev_time)  # Inverse of time difference
        prev_time = current_time

        # Show FPS on the video feed
        global font
        frame = cv2.flip(frame, 1)


        # Translate original frame to gray scale
        global face_filter
        # global eye_filter
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Detect faces in the image
        face_rects = face_filter.detectMultiScale(gray_frame, 1.3, 5)

        # Detect eyes, removes eyes that are not "on" the face
        eye_rects = eye_filter.detectMultiScale(gray_frame, 1.3, 5)
        filtered_eyes = []

        for (x_face, y_face, w_face, h_face) in face_rects:
            for (x_eye, y_eye, w_eye, h_eye) in eye_rects:
                if x_eye > x_face and (x_eye + w_eye) < (x_face + w_face) and \
                        y_eye > y_face and (y_eye + h_eye) < (y_face + h_face):
                    filtered_eyes.append((x_eye, y_eye, w_eye, h_eye))

        eye_rects = filtered_eyes

        # Draw faces and (valid) eyes rectangles
        for (x_face, y_face, w_face, h_face) in face_rects:
            cv2.rectangle(frame, (x_face, y_face), (x_face + w_face, y_face + h_face), (0, 255, 255), 3)

        for (x_eye, y_eye, w_eye, h_eye) in eye_rects:
            cv2.rectangle(frame, (x_eye, y_eye), (x_eye + w_eye, y_eye + h_eye), (0, 255, 0), 3)

        global eyes_are_open
        global warn_frame
        global eyes_closed_warning
        if len(eye_rects) == 0:
            eyes_are_open = False
            warn_frame += 1
            # print("Eyes are now closed!")
            if warn_frame > 5:
                warn_frame = 5
            if not eyes_closed_warning:
                if warn_frame == 5:
                    eyes_closed_warning = True
        else:
            eyes_are_open = True
            warn_frame -= 1
            # print("Eyes are now open!")
            if warn_frame < 0:
                warn_frame = 0
            if eyes_closed_warning:
                if warn_frame == 0:
                    eyes_closed_warning = False

        cv2.putText(frame, f'FPS: {int(fps)}', (10, 30), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
        frame = cv2.resize(frame, (small_canvas_width - 4, small_canvas_height - 4))
        frame_img = ImageTk.PhotoImage(Image.fromarray(frame))
        small_canvas.create_image(0, 0, anchor=tk.NW, image=frame_img)
        small_canvas.image = frame_img
    root.after(105, update_camera)

# Function to update the small canvas size and position
def update_small_canvas(event):
    global small_canvas_width, small_canvas_height
    # Adjust size of the small canvas relative to the main window size
    small_canvas_width = int(screen_width // 4)
    small_canvas_height = int(screen_height // 4)

    # Keep the small canvas positioned at the bottom-right
    # print("canvas position updated!")
    small_canvas.place(x=screen_width - small_canvas_width, y=screen_height - small_canvas_height)

# Initialize tkinter and set up window
root = tk.Tk()
root.title("Video and Camera Feed")

# Set initial window size (you can set a fixed size or adjust to the screen)
root.geometry("800x600")
root.attributes("-fullscreen", True)

# Get screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
small_canvas_width = screen_width // 4
small_canvas_height = screen_height // 4

# Create the main video canvas (filling entire screen)
video_canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg="black")
video_canvas.pack(fill=tk.BOTH, expand=True)

# Create the smaller camera canvas (will be placed in the bottom-right corner)
small_canvas = tk.Canvas(root, width=small_canvas_width, height=small_canvas_height, bg="white", bd=2)
small_canvas.place(x=screen_width - small_canvas_width, y=screen_height - small_canvas_height)

# Bind the window resize event to update the smaller canvas
root.bind("<Configure>", update_small_canvas)


# Start the update loops
update_video()
update_camera()


# Exit application with 'q' key
def keyboard_controls(event):
    global current_frame
    if event.char == "q":
        root.destroy()
    if event.char == "r":
        current_frame = 0
    if event.keysym == "space":
        global start_program
        if start_program is False:
            start_program = True
            global cap
            current_frame = 0
            cap = cv2.VideoCapture('./educational_materials/2.mp4')
            # Start the audio thread
            audio_thread = Thread(target=audio, args=('./educational_materials/2.wav',), daemon=True)
            audio_thread.start()



root.bind("<Key>", keyboard_controls)


# Run the tkinter main loop
root.mainloop()

# Release resources
cap.release()
camera.release()
cv2.destroyAllWindows()

