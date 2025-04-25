import cv2
import time

# Initialize variables
frame_count = 0  # Counter for frames saved
max_frames = 60# Maximum number of frames to extract
video_path = '../data/video1.mp4'  # Path to the input video
output_path = '../data/frames/'  # Path to save extracted frames

# Open the video file
cap = cv2.VideoCapture(video_path)

# Get the frame rate of the video
fps = int(cap.get(cv2.CAP_PROP_FPS))  # Frames per second of the video

# Ensure the video file is opened successfully
if not cap.isOpened():
    print("Error: Unable to open video file.")
    exit()

# Loop through the video frames
while frame_count < max_frames:
    # Read the next frame
    ret, frame = cap.read()
    if not ret:
        print("End of video or error reading frame.")
        break

    # Get the current frame position
    current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

    # Extract one frame per second
    if current_frame % fps == 0:
        # Resize the frame to the desired dimensions
        frame = cv2.resize(frame, (1080, 500))

        # Display the frame in a window (optional)
        cv2.imshow("Frame Preview", frame)

        # Save the frame as an image file
        frame_filename = f"{output_path}bag_{frame_count}.jpg"
        cv2.imwrite(frame_filename, frame)

        # Increment the frame counter
        frame_count += 1

        # Add a small delay (optional)
        time.sleep(0.01)

    # Exit if the user presses the 'Esc' key
    if cv2.waitKey(5) & 0xFF == 27:
        print("Exiting on user request.")
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
