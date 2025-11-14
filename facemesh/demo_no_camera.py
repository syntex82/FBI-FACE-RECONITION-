"""
Futuristic UI Demo without camera - uses simulated face detection
Perfect for testing when camera is not available
"""

import cv2
import numpy as np
import time
import math
from futuristic_ui import FuturisticUI

def create_simulated_face(frame, center_x, center_y, size=200):
    """Create a simulated face region that moves around."""
    x = int(center_x - size/2)
    y = int(center_y - size/2)
    w = size
    h = int(size * 1.3)  # Face is taller than wide
    
    # Keep within bounds
    x = max(0, min(x, frame.shape[1] - w))
    y = max(0, min(y, frame.shape[0] - h))
    
    return (x, y, w, h)

def create_simulated_landmarks(face_region, num_points=100):
    """Create simulated facial landmarks."""
    x, y, w, h = face_region
    landmarks = []
    
    # Create landmarks in a face-like pattern
    for i in range(num_points):
        # Distribute points across the face region
        angle = (i / num_points) * 2 * math.pi
        radius_x = w * 0.4
        radius_y = h * 0.4
        
        lx = x + w/2 + radius_x * math.cos(angle)
        ly = y + h/2 + radius_y * math.sin(angle)
        
        landmarks.append([lx, ly, 0])
    
    return np.array(landmarks)

def main():
    """Run the demo without camera."""
    print("=" * 70)
    print("FUTURISTIC UI DEMO - NO CAMERA MODE")
    print("=" * 70)
    print("\nThis demo simulates face detection without requiring a camera.")
    print("\nControls:")
    print("  SPACE - Change authentication status")
    print("  Q     - Quit")
    print("\nStarting demo...\n")
    
    ui = FuturisticUI()
    
    # Create a dark background
    width, height = 1280, 720
    
    # Animation variables
    frame_count = 0
    fps = 0
    last_time = time.time()
    frame_times = []
    
    # Face animation
    face_x = width // 2
    face_y = height // 2
    face_angle = 0
    
    # Status cycling
    statuses = ["SCANNING", "AUTHENTICATED", "DENIED", "NO FACE"]
    status_index = 0
    current_status = statuses[status_index]
    confidence = 0.85
    
    # User info
    user_info = {
        "User ID": "DEMO_USER",
        "Status": "AUTHENTICATED",
        "Access Level": "GRANTED",
        "Confidence": "85%"
    }
    
    while True:
        # Create frame
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Calculate FPS
        current_time = time.time()
        frame_times.append(current_time)
        frame_times = [t for t in frame_times if current_time - t < 1.0]
        fps = len(frame_times)
        
        # Animate face position (circular motion)
        face_angle += 0.02
        face_x = width // 2 + int(100 * math.cos(face_angle))
        face_y = height // 2 + int(50 * math.sin(face_angle))
        
        # Create simulated face
        face_region = create_simulated_face(frame, face_x, face_y, 250)
        landmarks = create_simulated_landmarks(face_region, 100)
        
        # Apply futuristic UI
        display = ui.draw_hud_frame(frame, "BIOMETRIC SYSTEM - DEMO MODE")
        
        if current_status != "NO FACE":
            display = ui.draw_face_grid(display, face_region)
            display = ui.draw_scanning_effect(display, face_region)
            display = ui.draw_landmark_points(display, landmarks, style="futuristic")
            display = ui.draw_face_box_advanced(display, face_region, current_status, confidence)
        
        # Draw metrics
        process_time = (time.time() - current_time) * 1000
        metrics = {
            "FPS": fps,
            "Process": f"{process_time:.1f}ms",
            "Users": 3,
            "Status": current_status
        }
        display = ui.draw_metrics_panel(display, metrics, position="right")
        
        # Draw user info if authenticated
        if current_status == "AUTHENTICATED":
            display = ui.draw_info_card(display, user_info, position=(20, 300))
        
        # Draw progress bar (simulated enrollment)
        progress = (math.sin(frame_count * 0.05) + 1) / 2  # Oscillate 0-1
        display = ui.draw_progress_bar(display, progress, (440, 650), 400, "SYSTEM STATUS")
        
        # Apply glow
        display = ui.apply_glow_effect(display, intensity=0.15)
        
        # Update animation
        ui.update_animation()
        frame_count += 1
        
        # Show frame
        cv2.imshow('Futuristic Biometric Demo (No Camera)', display)
        
        # Handle keys
        key = cv2.waitKey(30) & 0xFF
        
        if key == ord('q') or key == ord('Q'):
            break
        elif key == ord(' '):
            # Cycle through statuses
            status_index = (status_index + 1) % len(statuses)
            current_status = statuses[status_index]
            print(f"Status: {current_status}")
    
    cv2.destroyAllWindows()
    print("\n✓ Demo complete!")

if __name__ == "__main__":
    main()

