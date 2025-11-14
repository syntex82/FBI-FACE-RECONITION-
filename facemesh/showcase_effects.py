"""
Showcase all futuristic visual effects
Demonstrates each UI component individually
"""

import cv2
import numpy as np
import time
from futuristic_ui import FuturisticUI

def create_demo_image(width=1280, height=720):
    """Create a dark background image."""
    return np.zeros((height, width, 3), dtype=np.uint8)

def showcase_effects():
    """Showcase all visual effects one by one."""
    ui = FuturisticUI()
    
    effects = [
        ("HUD Frame", lambda img: ui.draw_hud_frame(img, "BIOMETRIC AUTHENTICATION SYSTEM")),
        ("Face Box - Scanning", lambda img: ui.draw_face_box_advanced(img, (400, 200, 300, 400), "SCANNING", 0.75)),
        ("Face Box - Authenticated", lambda img: ui.draw_face_box_advanced(img, (400, 200, 300, 400), "AUTHENTICATED", 0.95)),
        ("Face Box - Denied", lambda img: ui.draw_face_box_advanced(img, (400, 200, 300, 400), "DENIED", 0.30)),
        ("3D Grid Overlay", lambda img: ui.draw_face_grid(img, (400, 200, 300, 400))),
        ("Scanning Animation", lambda img: ui.draw_scanning_effect(img, (400, 200, 300, 400))),
        ("Metrics Panel", lambda img: ui.draw_metrics_panel(img, {
            "FPS": 30,
            "Process Time": 25.5,
            "Confidence": 0.85,
            "Status": "ACTIVE"
        }, "right")),
        ("Progress Bar", lambda img: ui.draw_progress_bar(img, 0.65, (440, 650), 400, "PROCESSING")),
        ("User Info Card", lambda img: ui.draw_info_card(img, {
            "User ID": "JOHN_DOE",
            "Status": "AUTHENTICATED",
            "Access Level": "GRANTED",
            "Confidence": "95%"
        }, (20, 300))),
        ("Glow Effect", lambda img: ui.apply_glow_effect(img, 0.25)),
    ]
    
    print("=" * 70)
    print("FUTURISTIC UI EFFECTS SHOWCASE")
    print("=" * 70)
    print("\nThis demo will show each visual effect individually.")
    print("Press any key to see the next effect, or 'Q' to quit.\n")
    
    for i, (name, effect_func) in enumerate(effects, 1):
        print(f"[{i}/{len(effects)}] Showing: {name}")
        
        # Create fresh image
        img = create_demo_image()
        
        # Apply effect
        img = effect_func(img)
        
        # Update animation for next frame
        ui.update_animation()
        
        # Show image
        cv2.imshow('Futuristic Effects Showcase', img)
        
        # Wait for key
        key = cv2.waitKey(0) & 0xFF
        if key == ord('q') or key == ord('Q'):
            print("\nShowcase ended by user.")
            break
    else:
        print("\n✓ All effects showcased!")
    
    # Show combined effect
    print("\nShowing all effects combined...")
    print("Press any key to continue...")
    
    img = create_demo_image()
    img = ui.draw_hud_frame(img, "ALL EFFECTS COMBINED")
    
    face_region = (400, 200, 300, 400)
    img = ui.draw_face_grid(img, face_region)
    img = ui.draw_scanning_effect(img, face_region)
    img = ui.draw_face_box_advanced(img, face_region, "AUTHENTICATED", 0.95)
    
    # Create fake landmarks
    landmarks = np.array([[x, y, 0] for x in range(400, 700, 30) for y in range(200, 600, 30)])
    img = ui.draw_landmark_points(img, landmarks, "futuristic")
    
    img = ui.draw_metrics_panel(img, {
        "FPS": 30,
        "Process": "25.5ms",
        "Users": 5,
        "Status": "ACTIVE"
    }, "right")
    
    img = ui.draw_info_card(img, {
        "User ID": "DEMO_USER",
        "Status": "AUTHENTICATED",
        "Access": "GRANTED"
    }, (20, 300))
    
    img = ui.draw_progress_bar(img, 0.85, (440, 650), 400, "SYSTEM READY")
    img = ui.apply_glow_effect(img, 0.15)
    
    cv2.imshow('Futuristic Effects Showcase', img)
    cv2.waitKey(0)
    
    cv2.destroyAllWindows()
    print("\n✓ Showcase complete!")
    print("\nTo see these effects in action with real face detection:")
    print("  python futuristic_demo.py")
    print("  python futuristic_app.py")

if __name__ == "__main__":
    showcase_effects()

