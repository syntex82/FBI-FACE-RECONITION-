"""
Capture images from camera for enrollment
Helps you easily capture multiple images of yourself or others for the FBI database
"""

import cv2
import os
from datetime import datetime

print("=" * 70)
print("FBI ENROLLMENT - IMAGE CAPTURE TOOL")
print("=" * 70)
print()

# Get person information
person_id = input("Enter Person ID (e.g., person_001): ").strip()
if not person_id:
    print("Error: Person ID required")
    exit(1)

person_name = input("Enter Person Name (e.g., John Doe): ").strip()
if not person_name:
    print("Error: Name required")
    exit(1)

# Create directory for images
image_dir = f"enrollment_images/{person_id}"
os.makedirs(image_dir, exist_ok=True)

print(f"\nImages will be saved to: {image_dir}")
print("\nInstructions:")
print("  - Look at the camera")
print("  - Press SPACE to capture an image")
print("  - Capture 3-5 images with slight variations:")
print("    * Different angles (slightly left, center, slightly right)")
print("    * Different expressions (neutral, slight smile)")
print("  - Press Q when done")
print("\nStarting camera...\n")

# Initialize camera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not cap.isOpened():
    print("Error: Could not open camera")
    exit(1)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

image_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break
    
    # Display frame
    display = frame.copy()
    
    # Add instructions
    cv2.putText(display, f"Capturing for: {person_name}", (10, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(display, f"Images captured: {image_count}", (10, 60),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(display, "SPACE = Capture | Q = Done", (10, 90),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
    
    # Draw face guide
    h, w = display.shape[:2]
    center_x, center_y = w // 2, h // 2
    guide_w, guide_h = 300, 400
    cv2.rectangle(display, 
                 (center_x - guide_w//2, center_y - guide_h//2),
                 (center_x + guide_w//2, center_y + guide_h//2),
                 (0, 255, 255), 2)
    cv2.putText(display, "Align face here", (center_x - 80, center_y - guide_h//2 - 10),
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    
    cv2.imshow('FBI Enrollment - Image Capture', display)
    
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord(' '):
        # Capture image
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{image_dir}/{person_id}_{image_count}_{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        image_count += 1
        print(f"✓ Captured image {image_count}: {filename}")
        
        # Flash effect
        flash = frame.copy()
        flash[:] = (255, 255, 255)
        cv2.imshow('FBI Enrollment - Image Capture', flash)
        cv2.waitKey(100)
        
    elif key == ord('q') or key == ord('Q'):
        break

cap.release()
cv2.destroyAllWindows()

print("\n" + "=" * 70)
print("IMAGE CAPTURE COMPLETE")
print("=" * 70)
print(f"\nCaptured {image_count} images for {person_name}")
print(f"Images saved to: {image_dir}")

if image_count > 0:
    print("\nNext step: Enroll these images into the FBI database")
    print(f"Run: python fbi_enroll.py")
    print(f"  - Select option 1 (Enroll from folder)")
    print(f"  - Enter Person ID: {person_id}")
    print(f"  - Enter Name: {person_name}")
    print(f"  - Enter folder path: {image_dir}")
else:
    print("\nNo images captured. Please try again.")

