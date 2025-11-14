"""
Quick test of the face detection system
"""

import cv2
from face_mesh_detector import FaceMeshDetector

print("Initializing face detector...")
detector = FaceMeshDetector()

print("Opening camera...")
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Could not open camera!")
    exit(1)

print("Camera opened successfully!")
print("Press 'q' to quit")
print("\nShowing live video with face detection...")

frame_count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break
    
    frame_count += 1
    
    # Detect and draw every frame
    annotated, landmarks = detector.detect_and_draw(frame)
    
    # Add frame counter
    cv2.putText(annotated, f"Frame: {frame_count}", (10, 30), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    if landmarks is not None:
        cv2.putText(annotated, f"Face Detected! ({len(landmarks)} faces)", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        print(f"Frame {frame_count}: Face detected!")
    else:
        cv2.putText(annotated, "No face detected", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    cv2.imshow('Face Detection Test', annotated)
    
    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
detector.close()

print("\nTest completed!")

