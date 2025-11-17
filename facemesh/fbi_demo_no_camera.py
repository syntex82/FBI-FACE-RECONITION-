"""
FBI System Demo - No Camera Required
Demonstrates the FBI-style interface without requiring a camera
"""

import cv2
import numpy as np
import time
import math
from fbi_ui import FBIUI


def create_sample_face_image(width=400, height=500, person_name="JOHN DOE"):
    """Create a sample face image for demonstration."""
    img = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Draw face outline (oval)
    center = (width // 2, height // 2)
    axes = (width // 3, height // 2 - 20)
    cv2.ellipse(img, center, axes, 0, 0, 360, (180, 180, 180), -1)
    
    # Draw eyes
    eye_y = height // 2 - 50
    left_eye = (width // 2 - 50, eye_y)
    right_eye = (width // 2 + 50, eye_y)
    cv2.circle(img, left_eye, 15, (50, 50, 50), -1)
    cv2.circle(img, right_eye, 15, (50, 50, 50), -1)
    
    # Draw nose
    nose_points = np.array([
        [width // 2, eye_y + 40],
        [width // 2 - 10, eye_y + 70],
        [width // 2 + 10, eye_y + 70]
    ])
    cv2.fillPoly(img, [nose_points], (150, 150, 150))
    
    # Draw mouth
    mouth_y = eye_y + 110
    cv2.ellipse(img, (width // 2, mouth_y), (40, 20), 0, 0, 180, (100, 100, 100), -1)
    
    # Add label
    cv2.putText(img, person_name, (10, height - 20),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
    
    return img


def main():
    """Run FBI demo without camera."""
    print("=" * 70)
    print("FBI FACIAL RECOGNITION SYSTEM - DEMO MODE (NO CAMERA)")
    print("=" * 70)
    print("\nThis demo showcases the FBI-style interface without a camera.")
    print("\nControls:")
    print("  SPACE - Cycle through match states")
    print("  Q     - Quit")
    print("\nStarting demo...\n")
    
    ui = FBIUI()
    
    # Create display
    width, height = 1400, 800
    
    # Demo states
    states = [
        ("SCANNING", None, 0.0),
        ("MATCH FOUND", "person_001", 0.95),
        ("MATCH FOUND", "person_002", 0.82),
        ("NO MATCH", None, 0.45),
    ]
    state_index = 0
    
    # Sample match data
    match_data_high = {
        "person_id": "person_001",
        "name": "JOHN DOE",
        "confidence": 0.95,
        "max_similarity": 0.97,
        "avg_similarity": 0.93,
        "num_images": 5,
        "is_match": True
    }
    
    match_data_medium = {
        "person_id": "person_002",
        "name": "JANE SMITH",
        "confidence": 0.82,
        "max_similarity": 0.85,
        "avg_similarity": 0.79,
        "num_images": 3,
        "is_match": True
    }
    
    # Recent matches for timeline
    recent_matches = [
        {"confidence": 0.95},
        {"confidence": 0.88},
        {"confidence": 0.76},
        {"confidence": 0.92},
        {"confidence": 0.68},
        {"confidence": 0.91},
        {"confidence": 0.85},
        {"confidence": 0.73},
    ]
    
    # Create sample images
    sample_img1 = create_sample_face_image(person_name="JOHN DOE")
    sample_img2 = create_sample_face_image(person_name="JANE SMITH")
    
    frame_count = 0
    
    while True:
        # Create frame
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Get current state
        status, person_id, confidence = states[state_index]
        
        # Draw FBI header
        frame = ui.draw_fbi_header(frame, "FBI FACIAL RECOGNITION SYSTEM - DEMO MODE")
        
        # Draw status indicator
        frame = ui.draw_status_indicator(frame, status, position=(20, 80))
        
        # Draw match info if applicable
        if status == "MATCH FOUND":
            if person_id == "person_001":
                match_data = match_data_high
                sample_img = sample_img1
            else:
                match_data = match_data_medium
                sample_img = sample_img2
            
            # Draw match info panel
            frame = ui.draw_match_info_panel(frame, match_data, position=(20, 150))
            
            # Draw confidence meter
            frame = ui.draw_confidence_meter(frame, match_data['confidence'], 
                                            position=(400, 150))
            
            # Draw sample image
            img_h, img_w = sample_img.shape[:2]
            frame[150:150+img_h, 770:770+img_w] = sample_img
            
            # Label
            cv2.putText(frame, "DATABASE IMAGE", (770, 140),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, ui.colors['fbi_gold'], 2, cv2.LINE_AA)
        
        # Draw database stats
        stats_text = [
            "DATABASE STATISTICS",
            "Persons: 15",
            "Images: 67",
            "Avg Images/Person: 4.5",
            "",
            f"FPS: 30",
            f"Frame: {frame_count}"
        ]
        
        y_pos = 80
        for text in stats_text:
            if text:
                cv2.putText(frame, text, (width - 280, y_pos),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, 
                           ui.colors['white'], 1, cv2.LINE_AA)
            y_pos += 25
        
        # Draw timeline
        frame = ui.draw_timeline(frame, recent_matches, 
                                position=(20, height - 120),
                                width=width - 40)
        
        # Update animation
        ui.update_animation()
        frame_count += 1
        
        # Show frame
        cv2.imshow('FBI Facial Recognition System - Demo', frame)
        
        # Handle keys
        key = cv2.waitKey(30) & 0xFF
        
        if key == ord('q') or key == ord('Q'):
            break
        elif key == ord(' '):
            state_index = (state_index + 1) % len(states)
            print(f"State: {states[state_index][0]}")
    
    cv2.destroyAllWindows()
    print("\n✓ Demo complete!")


if __name__ == "__main__":
    main()

