"""
Quick test of dashboard rendering
"""

import cv2
import numpy as np
from fbi_dashboard import FBIDashboard

print("Testing dashboard...")

# Create test dashboard
dashboard = FBIDashboard()

# Get Michael's profile
profile = dashboard.get_profile("michael")
if not profile:
    print("Error: Profile not found!")
    exit(1)

print(f"Found profile: {profile['full_name']}")

# Create test match data
match_data = {
    'person_id': 'michael',
    'name': 'Michael Blenkinsop',
    'confidence': 0.95,
    'is_match': True,
    'max_similarity': 0.97,
    'avg_similarity': 0.93
}

# Create dummy frame
frame = np.zeros((720, 1280, 3), dtype=np.uint8)

print("Rendering dashboard...")
try:
    display = dashboard.draw_dashboard(frame, profile, match_data)
    print(f"Dashboard rendered successfully! Size: {display.shape}")
    
    # Show it
    cv2.imshow('Dashboard Test', display)
    print("\nPress any key to close...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print("✓ Test complete")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

