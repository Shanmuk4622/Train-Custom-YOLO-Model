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

# Load image
image_path = "../data/frames/bag_11.jpg"  # Change to your image path
if not os.path.exists(image_path):
    raise FileNotFoundError(f"Image file '{image_path}' not found.")

frame = cv2.imread(image_path)
if frame is None:
    raise FileNotFoundError(f"Image file '{image_path}' could not be loaded.")

# Load class list
weights_file = "../weights/coco1.txt"
if not os.path.exists(weights_file):
    raise FileNotFoundError(f"Class list file '{weights_file}' not found.")

with open(weights_file, "r") as my_file:
    class_list = my_file.read().split("\n")

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

cv2.imshow("RGB", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

