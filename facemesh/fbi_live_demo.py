"""
FBI Live Demo - Real face detection without database
Shows face detection working in real-time with FBI interface
"""

import cv2
import numpy as np
from face_mesh_detector import FaceMeshDetector
from biometric_features import BiometricFeatureExtractor
from fbi_ui import FBIUI

print("=" * 70)
print("FBI LIVE DEMO - REAL FACE DETECTION")
print("=" * 70)
print("\nThis demo shows real-time face detection with FBI interface")
print("No database required - just testing face detection\n")
print("Controls:")
print("  Q - Quit")
print("\nStarting...\n")

# Initialize components
detector = FaceMeshDetector()
feature_extractor = BiometricFeatureExtractor()
ui = FBIUI()

# Initialize camera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not cap.isOpened():
    print("Error: Could not open camera")
    exit(1)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

frame_count = 0
faces_detected_total = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break
    
    # Detect faces
    landmarks_list = detector.detect(frame)
    
    # Create display
    display = frame.copy()
    
    # Draw FBI header
    display = ui.draw_fbi_header(display, "FBI LIVE DEMO - FACE DETECTION TEST")
    
    # Determine status
    if landmarks_list and len(landmarks_list) > 0:
        status = f"FACE DETECTED ({len(landmarks_list)} face(s))"
        faces_detected_total += 1
        
        # Draw face boxes
        for landmarks in landmarks_list:
            # Get face bounding box
            landmarks_array = np.array(landmarks)
            x_min = int(np.min(landmarks_array[:, 0]))
            y_min = int(np.min(landmarks_array[:, 1]))
            x_max = int(np.max(landmarks_array[:, 0]))
            y_max = int(np.max(landmarks_array[:, 1]))
            
            # Draw box
            cv2.rectangle(display, (x_min, y_min), (x_max, y_max), 
                         ui.colors['green'], 3)
            
            # Draw landmarks (sample)
            for i in range(0, len(landmarks), 10):
                x, y = int(landmarks[i][0]), int(landmarks[i][1])
                cv2.circle(display, (x, y), 2, ui.colors['fbi_gold'], -1)
            
            # Extract features
            features = feature_extractor.extract_features(landmarks)
            
            # Show feature count
            cv2.putText(display, f"Features: {len(features)}", 
                       (x_min, y_min - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, 
                       ui.colors['green'], 2)
    else:
        status = "SCANNING FOR FACES"
    
    # Draw status
    display = ui.draw_status_indicator(display, status, position=(20, 80))
    
    # Draw stats
    stats_text = [
        f"Frame: {frame_count}",
        f"Faces Detected: {faces_detected_total}",
        f"Current Faces: {len(landmarks_list) if landmarks_list else 0}",
        "",
        "DETECTION ACTIVE",
        "Look at camera to test"
    ]
    
    y_pos = 80
    for text in stats_text:
        if text:
            cv2.putText(display, text, (display.shape[1] - 300, y_pos),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, 
                       ui.colors['white'], 1, cv2.LINE_AA)
        y_pos += 25
    
    # Instructions
    cv2.putText(display, "This demo shows face detection is working", 
               (20, display.shape[0] - 60),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, ui.colors['yellow'], 2)
    cv2.putText(display, "To test matching: Enroll yourself, then run fbi_app.py", 
               (20, display.shape[0] - 30),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, ui.colors['yellow'], 2)
    
    # Update animation
    ui.update_animation()
    frame_count += 1
    
    # Show display
    cv2.imshow('FBI Live Demo - Face Detection', display)
    
    # Handle keys
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print("\n" + "=" * 70)
print("DEMO COMPLETE")
print("=" * 70)
print(f"\nTotal frames: {frame_count}")
print(f"Faces detected: {faces_detected_total}")
print("\nFace detection is working!")
print("\nNext steps:")
print("1. Capture images: python capture_enrollment_images.py")
print("2. Enroll person: python fbi_enroll.py")
print("3. Run FBI app: python fbi_app.py")

