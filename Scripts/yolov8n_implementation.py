##Imports and inputs
import cv2
from ultralytics import YOLO
import sys
import neoapi
import socket
import time
from cam_params import get_camera
# Input the width and height of the display window
window_width = 920
window_height = 640
# Define the height and width to crop from the top and left
crop_height = 250
crop_width = 50

# Define the server address and port in case you want to connect with a Raspberry Pi
# server_address = ('192.168.0.4', 65432)

#Load the model .pt file(pytorch weights)
model = YOLO("../Model/yolov8n_1.3k.pt")

## Initialize the camera or a video capture
# camera = get_camera()

video_path = '../Data/video002.avi' #Change with the relevant path to the video
cap = cv2.VideoCapture(video_path)

# Check if the video file opened successfully
if not cap.isOpened():
    print(f"Error: Could not open video file {video_path}")
    sys.exit()

##FUNCTIONS
# A function send a flag over the server, which can be interpreted as a signal to turn off the machine.
# def send_flag(flag):
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.connect(server_address)
#         s.sendall(str(flag).encode())

# Function to display stop message
def display_process_message(frame,text):
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.75
    color = (255, 0, 0)
    thickness = 2
    x, y = (300, 60)
    for line in text:
        cv2.putText(frame, line, (x, y), font, font_scale, color, thickness)
        y += 30
    return frame



# MAIN LOOP
while cap.isOpened():
    # send_flag(0)
    ret, img = cap.read()
    if not ret:
        print("End of video or error occurred.")
        break
    title = 'Live Feed...press ESC to exit ..'
    # img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    img = img[crop_height:, crop_width:]
    img = cv2.resize(img, (window_height, window_width))
    result = model(img)
    annotated_frame = result[0].plot()
    cv2.namedWindow(title, cv2.WINDOW_NORMAL) 
     # Draw a bounding box around the annotated image
    cv2.rectangle(annotated_frame, (200, 50), (620, 180), (0, 0, 0), -1)
    cv2.putText(annotated_frame, 'Monitoring..', (200, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    if not result[0].boxes.cls.numel() == 0:
        print("OBJECT DETECTED")
        #send_flag(1)
        annotated_frame = display_process_message(annotated_frame, ["Foreign element detected.", "Stopping Machine!", "Press Enter to continue.."])
        cv2.imshow(title, annotated_frame)
        while True:
            if cv2.waitKey(1) == 13:  # 13 is the Enter key
                break
        continue
    
    # Display the frame
    cv2.imshow(title, annotated_frame)
    print("entered")
    if cv2.waitKey(1) == 27:  # 27 is the ESC key
        # send_flag(1)
        break

# camera.Close()
cv2.destroyAllWindows()
