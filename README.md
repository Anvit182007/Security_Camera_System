# Security_Camera_System
This project is a real-time security surveillance system that uses face recognition and deep learning-based face detection to monitor individuals appearing in front of a camera. If an unrecognized person (intruder) is detected and remains in the frame for more than five seconds, the system captures an image and sends an alert via WhatsApp along with the intruder’s snapshot. Additionally, the system provides audio warnings using text-to-speech (TTS) technology to notify the intruder that they have been detected. This project is designed to enhance home security, office surveillance, and restricted area monitoring by automatically recognizing known individuals and detecting intruders.

Key Features
1️⃣ Real-Time Face Detection and Recognition
The system continuously captures video frames and detects faces using OpenCV’s deep learning-based DNN face detector (Caffe model). It then compares the detected faces with a stored "known" face using the face_recognition library.

2️⃣ Intruder Alert Mechanism
If an unrecognized face is detected for more than five seconds, the system captures an image and sends it to the registered user's WhatsApp number. Additionally, an audio warning saying, "You have been captured," is played using text-to-speech (TTS) technology.

3️⃣ Automated WhatsApp Notifications
The project uses the pywhatkit library to automatically send a WhatsApp message with an image of the intruder. This ensures that the user is notified immediately, even if they are not physically present at the monitored location.

4️⃣ Multi-Threaded Processing for Efficiency
To optimize performance and prevent lag, the project uses multi-threading, which allows the system to capture and process frames simultaneously without slowing down.

5️⃣ Date and Time Display on Video Feed
The system overlays the current date and time on the video feed, providing a timestamp for surveillance footage.

6️⃣ User-Friendly Interface
The system displays the live video feed with bounding boxes and labels indicating whether a face is recognized or unrecognized. It also allows the user to exit the program by pressing the 'q' key.

Technical Breakdown
📌 Face Recognition Process

The system first loads a reference image of the authorized user (e.g., "known.jpg").
It then captures real-time video from the webcam.
Using a pre-trained deep learning model (Caffe-based SSD), it detects faces in each frame.
It extracts the face encodings and compares them with the stored reference image to determine whether the face is recognized or unknown.
📌 Intruder Detection and Alert Workflow

If a detected face does not match the stored reference, it is labeled as "Unknown" (intruder).
The system starts a timer when an unknown face appears.
If the unknown face remains for more than five seconds, the system performs the following actions:
Captures a snapshot of the intruder.
Sends a WhatsApp alert with the image.
Plays an audio warning informing the intruder that they have been captured.
The system then resets the timer to avoid sending duplicate alerts.
📌 Performance Optimization

The system processes every alternate frame instead of every frame to reduce CPU load and improve efficiency.
Face detection and encoding run in a separate thread, allowing continuous video capture without slowing down the system.
Applications
🚀 Home Security – The system can be installed in homes to monitor unauthorized access and send instant alerts to the homeowner.

🚀 Office Surveillance – Businesses can use this project to track visitors and detect potential intruders in restricted areas.

🚀 Restricted Area Monitoring – Organizations can enforce security policies by allowing only authorized personnel to enter specific locations.

Conclusion
This AI-powered security system effectively combines computer vision, deep learning, and automation to provide an intelligent, real-time intruder detection mechanism. With features like WhatsApp notifications, face recognition, and audio warnings, the system ensures that users receive immediate alerts about any unauthorized access. This project enhances security by enabling quick responses to potential threats, making it an efficient and practical surveillance solution. 🚀
