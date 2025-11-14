"""
Test script for futuristic UI components
"""

import cv2
import numpy as np
from futuristic_ui import FuturisticUI

print("Testing Futuristic UI Components...")

# Create UI instance
ui = FuturisticUI()

# Create a test image
test_image = np.zeros((720, 1280, 3), dtype=np.uint8)

# Test 1: HUD Frame
print("✓ Testing HUD frame...")
test_image = ui.draw_hud_frame(test_image, "TEST SYSTEM")

# Test 2: Face box
print("✓ Testing face box...")
face_region = (400, 200, 300, 400)
test_image = ui.draw_face_box_advanced(test_image, face_region, "SCANNING", 0.85)

# Test 3: Grid overlay
print("✓ Testing grid overlay...")
test_image = ui.draw_face_grid(test_image, face_region)

# Test 4: Scanning effect
print("✓ Testing scanning effect...")
test_image = ui.draw_scanning_effect(test_image, face_region)

# Test 5: Metrics panel
print("✓ Testing metrics panel...")
metrics = {
    "FPS": 30,
    "Process Time": 25.5,
    "Confidence": 0.85,
    "Status": "ACTIVE"
}
test_image = ui.draw_metrics_panel(test_image, metrics, position="right")

# Test 6: Progress bar
print("✓ Testing progress bar...")
test_image = ui.draw_progress_bar(test_image, 0.65, (100, 650), width=300, label="PROCESSING")

# Test 7: Info card
print("✓ Testing info card...")
user_info = {
    "User ID": "TEST_USER",
    "Status": "AUTHENTICATED",
    "Access Level": "GRANTED"
}
test_image = ui.draw_info_card(test_image, user_info, position=(20, 300))

# Test 8: Glow effect
print("✓ Testing glow effect...")
test_image = ui.apply_glow_effect(test_image, intensity=0.15)

print("\n✓ All UI components tested successfully!")
print("\nDisplaying test image...")
print("Press any key to close...")

cv2.imshow('Futuristic UI Test', test_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

print("✓ Test complete!")

