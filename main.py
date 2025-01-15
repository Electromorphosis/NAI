import cv2
import time as t

video_path = "samples/blinking.mp4"
cap = cv2.VideoCapture(video_path)

face_cascPath = "pretrained/face_detector.xml"
eye_cascPath = "pretrained/eye_detector.xml"

face_filter = cv2.CascadeClassifier(face_cascPath)
eye_filter = cv2.CascadeClassifier(eye_cascPath)
if face_filter.empty() or eye_filter.empty():
    raise IOError("Where is my filter?!?!!")

while True:
    eyesOpen = False
    _, frame = cap.read()

    # Translate original frame to gray scale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Detect faces in the image
    face_rects = face_filter.detectMultiScale(gray_frame, 1.3, 5)
    eye_rects = eye_filter.detectMultiScale(gray_frame, 1.3, 5)

    for (x, y, w, h) in face_rects:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 3)

    for (x, y, w, h) in eye_rects:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    if len(eye_rects) == 0:
        cv2.putText(frame, "EYES ARE CLOSED!!!", (150, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0,0,255),2)

    cv2.imshow("Detection stream ", frame)
    t.sleep(0.03)
    # Closed when q is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

