import cv2
import time
import tkinter as tk
from PIL import Image, ImageTk

start_program = False

# Function to update the main video feed
def update_video():

    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (screen_width, screen_height))
        frame_img = ImageTk.PhotoImage(Image.fromarray(frame))
        video_canvas.create_image(0, 0, anchor=tk.NW, image=frame_img)
        video_canvas.image = frame_img
    else:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart video when it ends
    root.after(10, update_video)

# Function to update the live camera feed
def update_camera():
    ret, frame = camera.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (small_canvas_width-4, small_canvas_height-4))
        frame_img = ImageTk.PhotoImage(Image.fromarray(frame))
        small_canvas.create_image(0, 0, anchor=tk.NW, image=frame_img)
        small_canvas.image = frame_img
    root.after(10, update_camera)

# Function to update the small canvas size and position
def update_small_canvas(event):
    global small_canvas_width, small_canvas_height
    # Adjust size of the small canvas relative to the main window size
    small_canvas_width = int(screen_width // 4)
    small_canvas_height = int(screen_height // 4)

    # Keep the small canvas positioned at the bottom-right
    print("canvas position updated!")
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

# Open video file and camera
cap = cv2.VideoCapture('./downloads/start.jpg')  # Replace with your video path
camera = cv2.VideoCapture(0)  # 0 = default webcam

# Start the update loops
update_video()
update_camera()


# Exit application with 'q' key
def exit_app(event):
    if event.char == "q":
        root.destroy()

def start_program(event):
    global start_program
    if event.char == "space":
        if start_program is True:
            return
        else:
            start_program = True
            global cap
            cap = cv2.VideoCapture('./downloads/hamsters1.mp4')

root.bind("<Key>", exit_app)
root.bind("<Key>", start_program)


# Run the tkinter main loop
root.mainloop()

# Release resources
cap.release()
camera.release()
cv2.destroyAllWindows()


#
# video_path = "samples/blinking.mp4"
# cap = cv2.VideoCapture(video_path)
# # cap = cv2.VideoCapture(0)
#
# face_cascPath = "pretrained/face_detector.xml"
# eye_cascPath = "pretrained/eye_detector.xml"
#
# face_filter = cv2.CascadeClassifier(face_cascPath)
# eye_filter = cv2.CascadeClassifier(eye_cascPath)
# if face_filter.empty() or eye_filter.empty():
#     raise IOError("Where is my filter?!?!!")
#
# eyes_are_open = False
# eyes_closed_warning = False
# start_time = time.time()
#
# while True:
#     eyesOpen = False
#     _, frame = cap.read()
#
#     # Translate original frame to gray scale
#     gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     # Detect faces in the image
#     face_rects = face_filter.detectMultiScale(gray_frame, 1.3, 5)
#
#     # Detect eyes, removes eyes that are not "on" the face
#     eye_rects = eye_filter.detectMultiScale(gray_frame, 1.3, 5)
#     filtered_eyes = []
#
#     for (x_face, y_face, w_face, h_face) in face_rects:
#         for (x_eye, y_eye, w_eye, h_eye) in eye_rects:
#             if x_eye > x_face and (x_eye + w_eye) < (x_face + w_face) and \
#                     y_eye > y_face and (y_eye + h_eye) < (y_face + h_face):
#                 filtered_eyes.append((x_eye, y_eye, w_eye, h_eye))
#
#     eye_rects = filtered_eyes
#
#     # Draw faces and (valid) eyes rectangles
#     for (x_face, y_face, w_face, h_face) in face_rects:
#         cv2.rectangle(frame, (x_face, y_face), (x_face + w_face, y_face + h_face), (0, 255, 255), 3)
#
#     for (x_eye, y_eye, w_eye, h_eye) in eye_rects:
#         cv2.rectangle(frame, (x_eye, y_eye), (x_eye + w_eye, y_eye + h_eye), (0, 255, 0), 3)
#
#     if len(eye_rects) == 0:
#         cv2.putText(frame, "EYES ARE CLOSED!!!", (150, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
#                     (0,0,255),2)
#
#     cv2.imshow("Detection stream ", frame)
#     time.sleep(0.03)
#     # Closed when q is pressed
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# cap.release()
# cv2.destroyAllWindows()
#
