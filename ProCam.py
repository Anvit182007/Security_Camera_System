import cv2
import face_recognition
import threading
import numpy as np
import pywhatkit as kit
import time
import pyttsx3
from datetime import datetime

# Load your known image
your_image = face_recognition.load_image_file("known.jpg")
your_face_encoding = face_recognition.face_encodings(your_image)[0]

# Initialize video capture
video_capture = cv2.VideoCapture(0) 

# Load pre-trained DNN face detector (Caffe model)
net = cv2.dnn.readNetFromCaffe("deploy.prototxt", "res10_300x300_ssd_iter_140000.caffemodel")

frame_count = 0  # Track frame count
face_locations = []
face_encodings = []
frame_to_display = None  # This will hold the frame to be displayed
last_sent_time = 0  # Track time of last message to avoid spamming
intruder_detected_time = None  # Track time when intruder is first detected

# Your WhatsApp phone number (with country code, e.g., +11234567890)
your_phone_number = "+11234567890"  #enter your own number

# Function to send WhatsApp message along with image
def send_whatsapp_message(receiver, message, image_path):
    # Send the image with a message at once
    kit.sendwhats_image(receiver, image_path, message)

engine = pyttsx3.init()
rate = engine.getProperty('rate')
# Set a slightly slower rate (you can fine-tune this value)
engine.setProperty('rate', rate - 50)  # Decrease by 50 (default is usually around 200)

# Set properties (optional, for debugging purposes)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # 0 for male, 1 for female (depending on your system)

def say_warning():
    engine.say("You have been captured")  # The warning message
    engine.runAndWait()

# Function for face recognition
def process_frame(frame):
    global face_locations, face_encodings, frame_to_display
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Detect faces using the DNN-based detector
    blob = cv2.dnn.blobFromImage(rgb_frame, 1.0, (300, 300), (104.0, 177.0, 123.0), False, False)
    net.setInput(blob)
    detections = net.forward()
    
    face_locations = []
    face_encodings = []
    
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        
        if confidence > 0.5:  # Confidence threshold
            # Get coordinates of detected face
            box = detections[0, 0, i, 3:7] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
            (startX, startY, endX, endY) = box.astype("int")
            
            # Add face location
            face_locations.append((startY, endX, endY, startX))
            
            # Get face encoding for recognition
            face_encodings.append(face_recognition.face_encodings(rgb_frame, [(startY, endX, endY, startX)])[0])

    frame_to_display = frame   
    # Save the frame to be displayed by the main loop

# Thread function to capture frames
def capture_frame():
    global frame_count
    while True:
        ret, frame = video_capture.read()
        if ret:
            if frame_count % 2 == 0:  # Process every second frame
                process_frame(frame)  # Process the current frame
            frame_count += 1

# Start the capture thread
capture_thread = threading.Thread(target=capture_frame)
capture_thread.daemon = True  # Allow thread to exit when the program ends
capture_thread.start()

# Check for intruders and send message if needed
while True:
    if frame_to_display is not None:
        recognized_face_found = False
        intruders_detected = []  # Track detected intruders

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces([your_face_encoding], face_encoding)

            if True in matches:  # Match found (recognized face)
                color = (0, 255, 0)  # Green for recognized face
                label = "Your name"
                recognized_face_found = True
                intruder_detected_time = None  # Reset the timer if recognized face
            else:  # Unknown face (intruder)
                color = (0, 0, 255)  # Red for unknown face
                label = "Unknown"
                intruders_detected.append(label)  # Add intruder to the list

                if intruder_detected_time is None:  # If it's the first detection of the intruder
                    intruder_detected_time = time.time()

            # Draw the face box and label
            cv2.rectangle(frame_to_display, (left, top), (right, bottom), color, 2)
            cv2.putText(frame_to_display, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        # If an intruder is detected for more than 5 seconds, send a snapshot with message
        if intruder_detected_time is not None:
            current_time = time.time()
            if current_time - intruder_detected_time > 5:  # 5 seconds threshold
                # Say warning
                
                # Take snapshot and save it
                snapshot_path = "intruder_snapshot.jpg"
                cv2.imwrite(snapshot_path, frame_to_display)

                # Send WhatsApp message with image at once
                intruder_message = "Intruder detected!"
                send_whatsapp_message(your_phone_number, intruder_message, snapshot_path)
                
                say_warning() 

                # Reset the timer after sending the message
                intruder_detected_time = None

        # Add current date and time to the bottom-right corner without seconds
        now = datetime.now()
        current_time_text = now.strftime("%Y-%m-%d %H:%M")  # Removed seconds
        cv2.putText(frame_to_display, current_time_text, (frame_to_display.shape[1] - 250, frame_to_display.shape[0] - 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow('Security Camera', frame_to_display)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit on 'q'
        break

video_capture.release()
cv2.destroyAllWindows()
