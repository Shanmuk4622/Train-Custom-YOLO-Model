import cv2
import pandas as pd
from ultralytics import YOLO
import cvzone
import os

# Load YOLO model
model = YOLO('../weights/best.pt')

def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        point = [x, y]
        # print(point)

cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)

# Load video
video_path = "../data/video1.mp4"  # Change to your video path
if not os.path.exists(video_path):
    raise FileNotFoundError(f"Video file '{video_path}' not found.")

cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    raise FileNotFoundError(f"Video file '{video_path}' could not be opened.")

# Get the original FPS of the video
original_fps = cap.get(cv2.CAP_PROP_FPS)
frame_interval = int(original_fps / 20)  # Process only 10 frames per second

# Load class list
weights_file = "../weights/coco1.txt"
if not os.path.exists(weights_file):
    raise FileNotFoundError(f"Class list file '{weights_file}' not found.")

with open(weights_file, "r") as my_file:
    class_list = my_file.read().split("\n")

frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("End of video or cannot read the frame.")
        break

    # Skip frames to achieve 10 FPS processing
    if frame_count % frame_interval != 0:
        frame_count += 1
        continue

    frame_count += 1

    # Resize frame
    frame = cv2.resize(frame, (1020, 500))

    # Perform YOLO model prediction
    results = model.predict(frame)
    if not results or not results[0].boxes.data.size:
        print("No objects detected.")
    else:
        # Process detection results
        a = results[0].boxes.data
        px = pd.DataFrame(a).astype("float")

        for index, row in px.iterrows():
            x1 = int(row[0])
            y1 = int(row[1])
            x2 = int(row[2])
            y2 = int(row[3])
            d = int(row[5])
            c = class_list[d] if d < len(class_list) else "Unknown"

            # Draw bounding box and label
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
            cvzone.putTextRect(frame, f'{c}', (x1, y1), 1, 3)

    # Display the frame
    cv2.imshow("RGB", frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()

